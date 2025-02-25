import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-pro')

# Folder to save session data
SESSION_FOLDER = "sessions"
os.makedirs(SESSION_FOLDER, exist_ok=True)

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

def chat_with_law_assistant(session_id, user_input):
    # Load session data
    session_data = load_session(session_id)

    # Add the user input to the session history
    session_data.append({"role": "user", "text": user_input})

    # prompting examples
    examples = """
    Example 1:
    User: What is the difference between civil law and criminal law?
    Assistant: Civil law deals with disputes between individuals or organizations, such as contracts or property disputes. Criminal law, on the other hand, involves actions that are harmful to society and are prosecuted by the state, such as theft or assault.

    Example 2:
    User: Can a lawyer represent both parties in a case?
    Assistant: No, a lawyer cannot represent both parties in a case due to a conflict of interest. It is unethical and prohibited by legal professional standards.
    
    Example 2:
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
    You are a legal assistant specializing in Indian law, IPC section, justice, advocates, lawyers, official Passports, and judgment-related topics.
    You are an attorney and/or criminal lawyer to determine legal rights with full knowledge of IPC section, Indian Acts and government-related official work.
    Your task is to provide accurate, related IPC section numbers and Indian Acts, judgements, and professional answers to legal questions.
    If the question is not related to law or related to all the above options, politely decline to answer.

    Guidelines:
    - Provide answers in plain language that is easy to understand.
    - If the user asks a question in the local language, assist the user in the same language.
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
        return f"Error: {e}"

# Streamlit App
def main():
    st.title("Personalized Legal Assistant")
    st.write("Welcome to the Law Chat Assistant! Ask me anything about law, judiciary, justice, advocates, lawyers, or judgment-related topics.")

    # Session ID (you can make this dynamic if needed)
    session_id = "session_1"

    # Input from user
    #user_input = st.text_input("How can I assist you: ", "")
    user_input = st.text_area("How can I assist you: ", value="", height=300)

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Get the assistant's response
            response = chat_with_law_assistant(session_id, user_input)
            st.text_area("Assistant:", value=response, height=400)

            # Display conversation history
            #st.subheader("Conversation History")
            session_data = load_session(session_id)
            #for msg in session_data:
                #st.write(f"{msg['role'].capitalize()}: {msg['text']}")

if __name__ == "__main__":
    main()
    
