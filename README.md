# Pharmacy Intelligent System

The Pharmacy Intelligent System is a comprehensive application designed for hospital pharmacies, offering functionalities for managing inventory, processing orders, and interacting through a sophisticated chatbot. This document provides an overview of the project, setup instructions, and usage guidelines.

### Features

1. **Pharmacist Login and Dashboard**
   - Secure login with authentication against a MySQL database.
   - Personalized dashboard displaying pharmacist-specific functionalities.
   - Contain all patient data and analysis for this data 
2. **Inventory Management**
   - View, search, and edit drug inventory.
   - Add new drugs with specified quantity and dosage.

3. **Order Management**
   - View orders placed by patients.
   - Mark orders as "Taken" upon fulfillment and also check for paid or not paid to check the medicine.
   
4. **Interactive Chatbot**
   - Responds to natural language queries related to pharmacy database information.
   - Supports text input and speech recognition for user convenience and used to make data analysis.
   - Have full control on the system .

### Technologies Used

- **Frontend**: Streamlit for creating interactive web applications.
- **Backend**: Python with MySQL database for data storage and management.
- **Natural Language Processing**: Integrated with LangChain for generating SQL queries and processing chat responses.
- **Speech Recognition**: Utilized SpeechRecognition library for voice input processing.

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd pharmacy-intelligent-system
