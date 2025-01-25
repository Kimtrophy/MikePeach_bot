import os
import pdfplumber
import streamlit as st

# Step 1: Extract text from the PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} does not exist.")
        return ""

    try:
        # Open the PDF with pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Only add text if extraction is successful
                    text += page_text
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""  # Return empty string if extraction fails

# Step 2: Preprocess and structure the data (No changes here)
def preprocess_company_data(pdf_content):
    company_data = {
        "name": "MikePeach Oil and Gas Company",
        "address": "PLOT 30, OMUMAH IGWURUTA, ALONG CHOKOCHI ETCHE EXPRESS ROAD, IGWURUTA, Nigeria",
        "services": [
            "Gas Refilling: High-quality gas refilling for cylinders.",
            "Driver Assignments: Seamless pickup and delivery of gas cylinders.",
            "Delivery Services: Efficient delivery of refilled cylinders."
        ],
        "operating_hours": "Monday - Saturday: 9:00 AM - 5:00 PM",
        "mission": "To provide reliable, affordable, and accessible gas services to every corner of Nigeria.",
        "vision": "To be the foremost gas service provider in Nigeria, known for innovation, reliability, and outstanding customer service."
    }
    return company_data

# Step 3: Chatbot response function
def chatbot_response(question, company_data):
    question = question.lower().strip()  # Convert to lowercase and strip extra spaces
    print(f"User question: {question}")  # Debugging output

    # Handle greetings
    if question in ["hi", "hello", "hey"]:
        return "Hey!"
    elif question in ["how are you", "how are you doing", "how you doing"]:
        return "I am doing all well. How about you?"

    # Handle company-related questions
    if any(keyword in question for keyword in ["address", "location", "where", "situated", "located"]):
        return f"Our address is: {company_data['address']}"
    elif any(keyword in question for keyword in ["services", "offer", "provide"]):
        return "We offer the following services:\n" + "\n".join(company_data["services"])
    elif any(keyword in question for keyword in ["hours", "time", "open", "operating"]):
        return f"Our operating hours are: {company_data['operating_hours']}"
    elif any(keyword in question for keyword in ["mission", "goal", "objective"]):
        return f"Our mission: {company_data['mission']}"
    elif any(keyword in question for keyword in ["vision", "future"]):
        return f"Our vision: {company_data['vision']}"
    else:
        return "I'm sorry, I don't have an answer for that right now."

# Main application
def main():
    st.title("MikePeach Oil and Gas Chatbot")
    st.write("Ask me anything about MikePeach Oil and Gas Company!")

    # Initialize session state for storing chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # Extract and preprocess data
    pdf_path = "MikePeach_Oil_and_Gas_Company_Profile.pdf"
    pdf_content = extract_text_from_pdf(pdf_path)

    if not pdf_content:  # Check if PDF extraction was successful
        st.write("Sorry, I couldn't extract any text from the PDF.")
        return

    company_data = preprocess_company_data(pdf_content)

    # Display chat history
    if st.session_state.history:
        for message in st.session_state.history:
            st.write(message)  # Display previous messages

    # Chat interface: Dynamically updating user input
    user_question = st.text_input("Your question:", value=st.session_state.user_input)

    if user_question:
        # Generate response
        response = chatbot_response(user_question, company_data)
        
        # Add user input and chatbot response to history
        st.session_state.history.append(f"User: {user_question}")  
        st.session_state.history.append(f"Chatbot: {response}")  

        # Clear the input field by resetting session state for user_input
        st.session_state.user_input = ""  # Reset input field after the message is sent

        # Display chatbot's response
        st.write(response)

        # Optionally, ask if the user wants to end the session
        end_session = st.button("End Chat")
        if end_session:
            st.session_state.history = []  # Clear the chat history

if __name__ == "__main__":
    main()

