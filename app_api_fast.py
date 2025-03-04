import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Load API keys from .env
API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# Initialize the current key index in session state
if "current_key_index" not in st.session_state:
    st.session_state.current_key_index = 0

# Folder to save session data
SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)

# --- Helper Functions ---
def load_session(session_id):
    """Load session data from a file."""
    session_file = os.path.join(SESSION_FOLDER, f"{session_id}.json")
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            return json.load(f)
    return []

def save_session(session_id, session_data):
    """Save session data to a file."""
    session_file = os.path.join(SESSION_FOLDER, f"{session_id}.json")
    with open(session_file, "w") as f:
        json.dump(session_data, f)

def initialize_gemini():
    """Initialize Gemini with the current API key."""
    try:
        genai.configure(api_key=API_KEYS[st.session_state.current_key_index])
        return genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Error initializing Gemini: {e}")
        return None

def rotate_key():
    """Rotate to the next API key."""
    if st.session_state.current_key_index < len(API_KEYS) - 1:
        st.session_state.current_key_index += 1
        st.write(f"Switching to API key {st.session_state.current_key_index + 1}...")
        return initialize_gemini()
    else:
        st.error("All API keys have been used. Please add more keys.")
        return None

def chat_with_law_assistant(session_id, user_input):
    """Generate a response using Gemini and update session data."""
    global model  # Declare 'model' as global at the beginning of the function

    # Load session data
    session_data = load_session(session_id)

    # Add the user input to the session history
    session_data.append({"role": "user", "text": user_input})

    # Two-shot prompting examples
    examples = """
    Example 1:
    User: What is the difference between civil law and criminal law?
    Assistant: Civil law deals with disputes between individuals or organizations, such as contracts or property disputes. Criminal law, on the other hand, involves actions that are harmful to society and are prosecuted by the state, such as theft or assault.

    Example 2:
    User: Can a lawyer represent both parties in a case?
    Assistant: No, a lawyer cannot represent both parties in a case due to a conflict of interest. It is unethical and prohibited by legal professional standards.
    
    Example 3:
    User: Explain the process of filing a lawsuit in civil court.
    Assistant: Sure! Here's a step-by-step explanation:
    1. **Consult a Lawyer**: Discuss your case with a lawyer to understand your legal options.
    2. **Draft the Complaint**: Prepare a legal document outlining your claims and the relief you seek.
    3. **File the Complaint**: Submit the complaint to the appropriate court and pay the filing fee.
    4. **Serve the Defendant**: Notify the defendant about the lawsuit by serving them the complaint.
    5. **Await Response**: The defendant has a specified time to respond to the complaint.
    6. **Discovery Phase**: Both parties exchange information and evidence related to the case.
    7. **Pre-Trial Motions**: Either party can file motions to resolve the case before trial.
    8. **Trial**: If the case proceeds to trial, both parties present their arguments and evidence.
    9. **Judgment**: The judge or jury delivers a verdict.
    10. **Appeal**: If either party is dissatisfied, they can appeal the decision.
    """

    # Create a context-specific prompt
    prompt = f"""
    You are a legal assistant specializing in Indian law, IPC section, justice, advocates, lawyers, official Passport related, and judgment-related topics.
    You are an attorney and/or criminal lawyer to determine legal rights with full knowledge of IPC section, Indian Acts and government related official work.
    Your task is to provide accurate, related IPC sections number and Indian Acts, judgements, and professional answers to legal questions.
    If the question is not related to law or related to all above option, politely decline to answer.

    Guidelines:
    - Provide answers in plain language that is easy to understand.
    - If user asked question in local language, assistant user in same language.
    - If required for specific legal precedents or case law, provide relevant citations (e.g., case names, court, and year) along with a brief summary of the judgment.

    {examples}

    Conversation History:
    {" ".join([f"{msg['role']}: {msg['text']}" for msg in session_data])}

    User: {user_input}
    Assistant:
    """

    try:
        # Generate a response using the Gemini model
        response = model.generate_content(prompt)
        assistant_response = response.text

        # Add the assistant's response to the session history
        session_data.append({"role": "assistant", "text": assistant_response})

        # Save the updated session data
        save_session(session_id, session_data)

        return assistant_response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        # Rotate to the next key if the current one fails
        new_model = rotate_key()
        if new_model:
            model = new_model  # Update the global 'model' variable
            return chat_with_law_assistant(session_id, user_input)
        else:
            return "Sorry, I am unable to process your request at the moment."

# --- Streamlit App ---
def main():
    st.title("Personalized Legal Assistant")
    st.write("Welcome to the Law Chat Assistant! Ask me anything about law, judiciary, justice, advocates, lawyers, or judgment-related topics.")

    # Session ID (you can make this dynamic if needed)
    session_id = "session_1"

    # Input from user
    user_input = st.text_area("How can I assist you: ", value="", height=300)

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Get the assistant's response
            response = chat_with_law_assistant(session_id, user_input)
            st.text_area("Assistant:", value=response, height=400)

# Run the app
if __name__ == "__main__":
    # Initialize Gemini model
    model = initialize_gemini()
    if model:
        main()
