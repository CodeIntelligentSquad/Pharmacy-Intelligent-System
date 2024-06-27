import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import urllib.parse
import speech_recognition as sr
# Function to connect to the database
st.set_page_config(page_title="Chat with pharmacy pot", page_icon=":speech_balloon:")

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='P',
            user='root',
            password='3172004@mysql'
        )
        return connection
    except Error as e:
        st.error(f"Database Error: {e}")
        return None

def chatbot_page():
    def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
        encoded_password = urllib.parse.quote_plus(password)
        db_uri = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/{database}"
        return SQLDatabase.from_uri(db_uri)

    def get_sql_chain(db):
        template = """
            You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
            Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
            
            <SCHEMA>{schema}</SCHEMA>
            
            Conversation History: {chat_history}
            
            Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
            
            For example:
            Question: which 3 artists have the most tracks?
            SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
            Question: Name 10 artists
            SQL Query: SELECT Name FROM Artist LIMIT 10;
            
            Your turn:
            
            Question: {question}
            SQL Query:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        
        def get_schema(_):
            return db.get_table_info()
        
        return (
            RunnablePassthrough.assign(schema=get_schema)
            | prompt
            | llm
            | StrOutputParser()
        )

    def classify_question(question: str) -> bool:
        """
        Dummy classifier to determine if a question is related to the database.
        Always return True.
        """
        return True

    def get_response(user_query: str, db: SQLDatabase, chat_history: list):
        sql_chain = get_sql_chain(db)
        
        template = """
            You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
            Based on the table schema below, question, sql query, and sql response, write a natural language response.
            <SCHEMA>{schema}</SCHEMA>

            Conversation History: {chat_history}
            SQL Query: <SQL>{query}</SQL>
            User question: {question}
            SQL Response: {response}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        
        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                response=lambda vars: db.run(vars["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return chain.invoke({
            "question": user_query,
            "chat_history": chat_history,
        })

    def recognize_speech():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            st.info("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            st.info("Recognizing...")
            query = recognizer.recognize_google(audio)
            st.success(f"Recognized: {query}")
            return query
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a Pharmacist Assistant. Ask me anything about your pharmacy database."),
        ]

    if "db" not in st.session_state:
        st.session_state.db = None

    load_dotenv()

    st.title("Chat with pharmacy bot")

    with st.sidebar:
        st.image("Code\Phar.jpg", width=100)
        
        
        st.subheader("Settings")
        st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")
        
        
        host = st.text_input("Host", value="localhost", key="Host")
        port = st.text_input("Port", value="3306", key="Port")
        user = st.text_input("User", value="root", key="User")
        password = st.text_input("Password", value="3172004@mysql", key="Password")
        database = st.text_input("Database", value="P", key="Database")
        
        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
        
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        if st.session_state.db:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            
            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
                st.markdown(response)
                
            st.session_state.chat_history.append(AIMessage(content=response))
        else:
            st.error("Please connect to the database first.")

    if st.button("Speak a message"):
        spoken_query = recognize_speech()
        if spoken_query:
            if st.session_state.db:
                st.session_state.chat_history.append(HumanMessage(content=spoken_query))
                
                with st.chat_message("Human"):
                    st.markdown(spoken_query)
                    
                with st.chat_message("AI"):
                    response = get_response(spoken_query, st.session_state.db, st.session_state.chat_history)
                    st.markdown(response)
                    
                st.session_state.chat_history.append(AIMessage(content=response))
            else:
                st.error("Please connect to the database first.")

        
    
    
# Main Application
def main():
    st.title("Hospital Pharmacy Management System")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'pharmacist_id' not in st.session_state:
        st.session_state['pharmacist_id'] = ''
    if 'pharmacist_name' not in st.session_state:
        st.session_state['pharmacist_name'] = ''

    if st.session_state['logged_in']:
        pharmacist_dashboard()
    else:
        pharmacist_login()

# Pharmacist Login
def pharmacist_login():
    st.subheader("Pharmacist Login")
    
    with st.form(key='login_form'):
        pharmacist_id = st.text_input("Pharmacist ID")
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            if pharmacist_id:
                try:
                    conn = connect_to_db()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT Pharmacist_Name FROM pharmacist WHERE Pharmacist_ID = %s", (pharmacist_id,))
                        pharmacist = cursor.fetchone()
                        _ = conn.close()  # Suppress output by assigning to _
                        if pharmacist:
                            st.success("Valid Pharmacist ID")
                            st.session_state['logged_in'] = True
                            st.session_state['pharmacist_id'] = pharmacist_id
                            st.session_state['pharmacist_name'] = pharmacist[0]  # Store pharmacist name
                        else:
                            st.error("Invalid Pharmacist ID")
                    else:
                        st.error("Connection to the database failed")
                except Error as e:
                    st.error(f"Database Error: {e}")
            else:
                st.warning("Please enter Pharmacist ID")

# Pharmacist Dashboard
def pharmacist_dashboard():
    menu = ["Home", "Manage Inventory", "Add Drug", "View Orders", "Chatbot", "Logout"]  # Add "Chatbot" option
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write(f"Welcome, {st.session_state['pharmacist_name']}")  # Display pharmacist name
        st.write("This system allows you to manage patient records efficiently. You can perform the following tasks:")
        st.markdown("- User Authentication: Pharmacists can securely log in using their unique ID, ensuring that only authorized personnel can access the system.")
        st.markdown("- Inventory Management: Pharmacists can efficiently manage the inventory of medicines by adding new drugs, viewing existing drugs, editing drug details (such as quantity and dose), and removing drugs from the inventory.")
        st.markdown("- Order Tracking: Pharmacists can track orders placed by patients, search for specific patients by name or ID, view the details of each order, and mark orders as \"Taken\" once they have been fulfilled.")
        st.markdown("- Session Management: The system maintains session state for logged-in pharmacists, allowing them to navigate between different functionalities without the need for repeated logins. Session data is cleared securely upon logout.")

    elif choice == "Manage Inventory":
        manage_inventory()

    elif choice == "Add Drug":
        add_drug_page()

    elif choice == "View Orders":
        view_orders()

    elif choice == "Chatbot":  # Add condition for Chatbot option
        chatbot_page()  # Call the Chatbot page function

    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['pharmacist_id'] = ''
        st.session_state['pharmacist_name'] = ''  # Clear pharmacist name from session state
        st.experimental_rerun()


# Manage Inventory
def manage_inventory():
    st.subheader("Manage Inventory")
    
    search_term = st.text_input("Search for Medicine", value="")
    if search_term:
        filter_drugs(search_term)
    else:
        load_all_drugs()

def load_all_drugs():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT drug_id, Drug_Name, Quantity, Dose FROM drugs")
            drugs = cursor.fetchall()
            for drug in drugs:
                st.write(f"ID: {drug[0]}, Name: {drug[1]}, Quantity: {drug[2]}, Dose: {drug[3]}")
                if st.button(f"Edit {drug[1]}"):
                    open_edit_window(drug[0], drug[1], drug[2], drug[3])
            _ = conn.close()  # Suppress output by assigning to _
        except Error as e:
            st.error(f"Database Error: {str(e)}")

def filter_drugs(query):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT drug_id, Drug_Name, Quantity, Dose FROM drugs WHERE LOWER(Drug_Name) LIKE %s OR LOWER(CAST(drug_id AS CHAR)) LIKE %s", (f'%{query}%', f'%{query}%'))
            drugs = cursor.fetchall()
            for drug in drugs:
                st.write(f"ID: {drug[0]}, Name: {drug[1]}, Quantity: {drug[2]}, Dose: {drug[3]}")
                if st.button(f"Edit {drug[1]}"):
                    open_edit_window(drug[0], drug[1], drug[2], drug[3])
            _ = conn.close()  # Suppress output by assigning to _
        except Error as e:
            st.error(f"Database Error: {str(e)}")
        finally:
            _ = conn.close()  # Suppress output by assigning to _

def open_edit_window(drug_id, drug_name, quantity, dose):
    st.subheader(f"Edit {drug_name}")

    new_quantity = st.text_input("Quantity", value=str(quantity))
    new_dose = st.text_input("Dose", value=str(dose))

    if st.button("Save Changes"):
        save_drug_changes(drug_id, new_quantity, new_dose)

    if st.button("Delete Drug"):
        remove_drug_by_id(drug_id)

def save_drug_changes(drug_id, quantity, dose):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE drugs SET Quantity = %s, Dose = %s WHERE drug_id = %s", (quantity, dose, drug_id))
            conn.commit()
            st.success(f"Drug {drug_id} updated successfully.")
        except Error as e:
            st.error(f"Database Error: {str(e)}")
        finally:
            _ = conn.close()  # Suppress output by assigning to _

# Add Drug Page
def add_drug_page():
    st.subheader("Add Drug")
    
    drug_name = st.text_input("Drug Name")
    quantity = st.text_input("Quantity")
    dose = st.text_input("Dose")
    expiration_day = st.text_input("Expiration Day (YY-MM-DD)")
    manufacturer = st.text_input("Manufacturer")
    active_ingredients = st.text_input("Active Ingredients (comma-separated)")

    if st.button("Add Drug"):
        active_ingredients_list = [ing.strip() for ing in active_ingredients.split(',') if ing.strip()]
        add_drug(drug_name, quantity, dose, expiration_day, manufacturer, active_ingredients_list)


def add_drug(name, quantity, dose, expiration_day, manufacturer, active_ingredients):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Insert drug details into drugs table
            cursor.execute("INSERT INTO drugs (Drug_Name, Quantity, Dose, Expiration_date, Manufacturer) VALUES (%s, %s, %s, %s, %s)",
                           (name, quantity, dose, expiration_day, manufacturer))
            conn.commit()

            # Retrieve the last inserted Drug_ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            drug_id = cursor.fetchone()[0]

            # Insert active ingredients into drug_active_ingredients table
            for ingredient in active_ingredients:
                cursor.execute("INSERT INTO active_ingredients (Drug_ID, Active_ingredient) VALUES (%s, %s)",
                               (drug_id, ingredient))
            conn.commit()

            st.success(f"Drug {name} added successfully.")
        except Error as e:
            st.error(f"Database Error: {str(e)}")
        finally:
            _ = conn.close()  # Suppress output by assigning to _


def remove_drug_by_id(drug_id):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM drugs WHERE drug_id = %s", (drug_id,))
            conn.commit()
            st.success(f"Drug ID {drug_id} removed successfully.")
        except Error as e:
            st.error(f"Database Error: {str(e)}")
        finally:
            _ = conn.close()  # Suppress output by assigning to _

# View Orders
def view_orders():
    st.subheader("View Orders")
    if 'pharmacist_id' not in st.session_state:
        st.warning("Please login as a pharmacist first")
        return
    
    search_term = st.text_input("Search Patients", value="")
    if search_term:
        filter_patients(search_term)
    else:
        load_all_patients()

def load_all_patients():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Patient_ID, Patient_Name FROM patient")
            patients = cursor.fetchall()
            for patient in patients:
                if st.button(f"View Orders for {patient[1]} (ID: {patient[0]})"):
                    show_patient_orders(patient[0])
            _ = conn.close()  # Suppress output by assigning to _
        except Error as e:
            st.error(f"Database Error: {str(e)}")

def filter_patients(query):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Patient_ID, Patient_Name FROM patient WHERE Patient_Name LIKE %s OR Patient_ID LIKE %s", (f'%{query}%', f'%{query}%'))
            patients = cursor.fetchall()
            for patient in patients:
                if st.button(f"View Orders for {patient[1]} (ID: {patient[0]})"):
                    show_patient_orders(patient[0])
            _ = conn.close()  # Suppress output by assigning to _
        except Error as e:
            st.error(f"Database Error: {str(e)}")

def show_patient_orders(patient_id):
    st.subheader(f"Orders for Patient ID {patient_id}")
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Order_ID, Drug_Name, Quantity, Dose FROM orders WHERE Patient_ID=%s", (patient_id,))
            orders = cursor.fetchall()
            if orders:
                for order in orders:
                    st.write(f"Order ID: {order[0]}, Drug Name: {order[1]}, Quantity: {order[2]}, Dose: {order[3]}, Status: Not Taken")
                    if st.button(f"Mark as Taken for Order ID {order[0]}"):
                        mark_as_taken(order[0], patient_id)
            else:
                st.write("No orders found for this patient.")
            _ = conn.close()  # Suppress output by assigning to _
        except Error as e:
            st.error(f"Database Error: {str(e)}")

def mark_as_taken(order_id, patient_id):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET Status = 'Taken' WHERE Order_ID = %s", (order_id,))
            conn.commit()
            st.success(f"Order ID {order_id} marked as taken.")
            show_patient_orders(patient_id)
        except Error as e:
            st.error(f"Database Error: {str(e)}")
        finally:
            _ = conn.close()  # Suppress output by assigning to _



if __name__ == "__main__":
    main()
