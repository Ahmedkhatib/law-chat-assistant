# Law Chat Assistant 🧑‍⚖️

The **Law Chat Assistant** is a Streamlit-based web application that provides legal assistance on topics related to law, judiciary, justice, advocates, lawyers, and judgment-related matters. It uses the **Google Gemini Pro** model to generate accurate and professional responses to user queries.

---

## Features

- **Legal Expertise**: Specializes in law, judiciary, justice, advocates, lawyers, and judgment-related topics.
- **Session-Wise Conversations**: Saves conversation history for each session.
- **Two-Shot Prompting**: Includes examples to guide the model's behavior.
- **User-Friendly Interface**: Built with Streamlit for an interactive and intuitive experience.

---

## How It Works

1. The user enters a legal-related question in the input box.
2. The app sends the question to the **Google Gemini Pro** model via its API.
3. The model generates a response based on the input and conversation history.
4. The response is displayed to the user, and the conversation is saved for future reference.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A **Google Gemini API key** (get it from [Google AI Studio](https://makersuite.google.com/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmedkhatib/law-chat-assistant.git
   cd law-chat-assistant
