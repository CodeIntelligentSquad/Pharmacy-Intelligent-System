import streamlit as st
import requests
import mysql.connector
from itertools import combinations

# Helper function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='P'
    )

# Fetch all drugs and their active ingredients from the database
def get_all_drugs_from_db():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT d.Drug_ID, d.Drug_Name, ai.Active_ingredient
            FROM drugs d
            JOIN active_ingredients ai ON d.Drug_ID = ai.Drug_ID
        """)
        drugs = cursor.fetchall()
        cursor.close()
        connection.close()
        return drugs
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []

# Fetch all diagnoses from the database
def get_all_diagnoses_from_db():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT diagnosis_id, diagnosis_content FROM diagnosis")
        diagnoses = cursor.fetchall()
        cursor.close()
        connection.close()
        return diagnoses
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []

# Fetch alternative drugs based on active ingredient
def get_alternative_drugs(active_ingredient, current_drug_name):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT d.Drug_Name
            FROM drugs d
            JOIN active_ingredients ai ON d.Drug_ID = ai.Drug_ID
            WHERE ai.Active_ingredient = %s AND d.Drug_Name != %s
        """, (active_ingredient, current_drug_name))
        alternatives = cursor.fetchall()
        cursor.close()
        connection.close()
        return [alt[0] for alt in alternatives]
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return []

# Perform Google Custom Search
def search_google(query, api_key, search_id):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {'q': query, 'key': api_key, 'cx': search_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Classify the interaction from the search snippet
def classify_interaction(snippet):
    if "major" in snippet.lower():
        return "Major"
    elif "moderate" in snippet.lower():
        return "Moderate"
    elif "minor" in snippet.lower():
        return "Minor"
    else:
        return "No interaction specified"

# Add a new entry to the given list
def add_entry(entries):
    entries.append({'id': '', 'name': '', 'ingredient': ''})

# Delete an entry from the given list by index
def delete_entry(entries, index):
    if 0 <= index < len(entries):
        entries.pop(index)

# Streamlit interface to handle drug entries
def handle_drug_entries():
    st.header("Drug-Drug Interaction")
    if 'drug_entries' not in st.session_state:
        st.session_state.drug_entries = []
    if st.button("Add Drug Entry"):
        add_entry(st.session_state.drug_entries)

    all_drugs = get_all_drugs_from_db()
    drug_options = {f"{drug[0]} - {drug[1]}": (drug[0], drug[1], drug[2]) for drug in all_drugs}

    for index, entry in enumerate(st.session_state.drug_entries.copy()):
        cols = st.columns([1, 3, 4, 3])
        with cols[0]:
            if st.button("Delete Drug", key=f"delete_drug_{index}"):
                delete_entry(st.session_state.drug_entries, index)
                st.experimental_rerun()
        with cols[1]:
            selected_drug = st.selectbox("Choose Drug", options=[""] + list(drug_options.keys()), key=f"select_drug_{index}")
            if selected_drug:
                entry['id'], entry['name'], entry['ingredient'] = drug_options[selected_drug]
        with cols[2]:
            entry['id'] = st.text_input("Drug ID", value=entry['id'], key=f"drug_id_{index}")
        with cols[3]:
            entry['name'] = st.text_input("Drug Name", value=entry['name'], key=f"drug_name_{index}")

# Streamlit interface to handle diagnosis entries
def handle_diagnosis_entries():
    st.header("Drug-Diagnosis Interaction")
    if 'diagnosis_entries' not in st.session_state:
        st.session_state.diagnosis_entries = []
    if st.button("Add Diagnosis Entry"):
        add_entry(st.session_state.diagnosis_entries)

    all_diagnoses = get_all_diagnoses_from_db()
    diagnosis_options = {f"{diagnosis[0]} - {diagnosis[1]}": (diagnosis[0], diagnosis[1]) for diagnosis in all_diagnoses}

    for index, entry in enumerate(st.session_state.diagnosis_entries.copy()):
        cols = st.columns([1, 3, 4, 3])
        with cols[0]:
            if st.button("Delete Diagnosis", key=f"delete_diagnosis_{index}"):
                delete_entry(st.session_state.diagnosis_entries, index)
                st.experimental_rerun()
        with cols[1]:
            selected_diagnosis = st.selectbox("Choose Diagnosis", options=[""] + list(diagnosis_options.keys()), key=f"select_diagnosis_{index}")
            if selected_diagnosis:
                entry['id'], entry['name'] = diagnosis_options[selected_diagnosis]
        with cols[2]:
            entry['id'] = st.text_input("Diagnosis ID", value=entry['id'], key=f"diagnosis_id_{index}")
        with cols[3]:
            entry['name'] = st.text_input("Diagnosis Name", value=entry['name'], key=f"diagnosis_name_{index}")

# Search for interactions and display results
def search_interactions(API_KEY, SEARCH_ID):
    interactions_found = False
    displayed_explanations = set()

    if len(st.session_state.drug_entries) < 2 and not st.session_state.diagnosis_entries:
        st.warning("Please add at least two drug entries for Drug-Drug Interaction search or at least one drug and one diagnosis for Drug-Diagnosis Interaction search.")
        return

    # Drug-Drug Interactions
    valid_drug_entries = [entry for entry in st.session_state.drug_entries if entry['name']]
    if len(valid_drug_entries) >= 2:
        drug_pairs = combinations(valid_drug_entries, 2)
        for pair in drug_pairs:
            query1, query2 = pair[0]['name'], pair[1]['name']
            search_query = f"{query1} {query2} interaction site:drugs.com"
            results = search_google(search_query, API_KEY, SEARCH_ID)
            if results and 'items' in results:
                for item in results['items']:
                    title = item.get('title')
                    link = item.get('link')
                    snippet = item.get('snippet')
                    interaction_type = classify_interaction(snippet)
                    explanation_key = (query1, query2, snippet)
                    if explanation_key not in displayed_explanations:
                        displayed_explanations.add(explanation_key)
                        if interaction_type != "No interaction specified":
                            interactions_found = True
                            st.markdown(f"**Interaction between {query1} and {query2}:**")
                            st.markdown(f"**Interaction Type:** {interaction_type}")
                            st.markdown(f"**Explanation:** {snippet}")
                            st.markdown(f"[Reference: {title}]({link})")
                            st.write("---")

                            # Substitute with active ingredients if interaction found
                            for entry in st.session_state.drug_entries:
                                if entry['name'] == query1 or entry['name'] == query2:
                                    active_ingredient = entry['ingredient']
                                    entry['name'] = entry['ingredient']
                                    entry['id'] = f"Active Ingredient: {entry['ingredient']}"

                                    # Suggest alternatives based on active ingredient
                                    alternatives = get_alternative_drugs(entry['ingredient'], entry['name'])
                                    if alternatives:
                                        if alternatives[0] != entry['name']:
                                            entry['name'] = alternatives[0]
                                            entry['id'] = f"Drug ID: {alternatives[0]}"
                                        else:
                                            st.markdown(f"No alternatives found for {entry['name']}")
                                    else:
                                        st.markdown(f"No alternatives found for {entry['name']}")

    # Drug-Diagnosis Interactions
    valid_diagnosis_entries = [entry for entry in st.session_state.diagnosis_entries if entry['name']]
    if valid_drug_entries and valid_diagnosis_entries:
        for drug in valid_drug_entries:
            for diagnosis in valid_diagnosis_entries:
                query1, query2 = drug['name'], diagnosis['name']
                search_query = f"{query1} {query2} interaction site:drugs.com"
                results = search_google(search_query, API_KEY, SEARCH_ID)
                if results and 'items' in results:
                    for item in results['items']:
                        title = item.get('title')
                        link = item.get('link')
                        snippet = item.get('snippet')
                        interaction_type = classify_interaction(snippet)
                        explanation_key = (query1, query2, snippet)
                        if explanation_key not in displayed_explanations:
                            displayed_explanations.add(explanation_key)
                            if interaction_type != "No interaction specified":
                                interactions_found = True
                                st.markdown(f"**Interaction between {query1} and {query2}:**")
                                st.markdown(f"**Interaction Type:** {interaction_type}")
                                st.markdown(f"**Explanation:** {snippet}")
                                st.markdown(f"[Reference: {title}]({link})")
                                st.write("---")

                                # Suggest alternatives based on active ingredient
                                alternatives = get_alternative_drugs(drug['ingredient'], drug['name'])
                                if alternatives:
                                    if alternatives[0] != drug['name']:
                                        drug['name'] = alternatives[0]
                                        drug['id'] = f"Drug ID: {alternatives[0]}"
                                    else:
                                        st.markdown(f"No alternatives found for {drug['name']}")
                                else:
                                    st.markdown(f"No alternatives found for {drug['name']}")

    if not interactions_found:
        st.warning("No significant interactions found among the entered drugs and diagnoses.")

# Main function to handle Streamlit app flow
def main():
    with open('API_KEY') as f:
        API_KEY = f.read().strip()
    with open('SEARCH_ID') as f:
        SEARCH_ID = f.read().strip()

    st.title("Drug Interaction and Diagnosis Interaction Search")

    handle_drug_entries()
    handle_diagnosis_entries()

    if st.button("Search Interactions"):
        search_interactions(API_KEY, SEARCH_ID)

if __name__ == "__main__":
    main()
