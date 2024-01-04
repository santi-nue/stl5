import streamlit as st
import openai
import json
import os
from datetime import datetime

# Konfigurieren Sie Ihre OpenAI API-Einstellungen
openai.api_base = 'http://localhost:12347/v1'
openai.api_key = ''

# Ihre Funktion zur Abrufung von Vervollständigungen
def get_completion(prompt, model="local model", temperature=0.0):
    prefix = "### Instruction:\n"
    suffix = "\n### Response:"
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    messages = [{"role": "user", "content": formatted_prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

# Funktion für die Session-Liste
def save_session_index(session_key):
    try:
        with open(os.path.join('chat_data', 'session_index.json'), 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    session_index.append({
        "name": session_key,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": f'{session_key}_chat_history.json'
    })
    with open(os.path.join('chat_data', 'session_index.json'), 'w') as f:
        json.dump(session_index, f)

def app():
    st.title("Jarvis Chatbot")
    # Unterordner bei Bedarf für JSON-Dateien erstellen
    os.makedirs('chat_data', exist_ok=True)

    # Sidebar
    st.sidebar.title("Neuer Chat")
    neuer_chat_name = st.sidebar.text_input("Name für neuen Chat:", value="Chatname?", key="neuer_chat_name_sidebar")
  
    if st.sidebar.button("Neuer Chat"):
        st.session_state['session_key'] = neuer_chat_name
        save_chat_history(st.session_state['session_key'], [])  # Erstelle eine neue leere Chatverlauf-Datei
        save_session_index(st.session_state['session_key'])

    st.sidebar.markdown("---")  # Trennlinie
    st.sidebar.header("Chatverlauf")  # Überschrift

    # Liste vorhandener Chats
    try:
        with open(os.path.join('chat_data', 'session_index.json'), 'r') as f:
            session_index = json.load(f)
    except FileNotFoundError:
        session_index = []
    for session in session_index:
        if st.sidebar.button(session["name"]):
            st.session_state['session_key'] = session["name"]

    
    # Lade den Chatverlauf
    if 'session_key' in st.session_state:
        st.header(st.session_state['session_key'])  # Zeigt den Namen der aktuellen Session an
        chat_history = load_chat_history(st.session_state['session_key'])
        
        user_input = st.chat_input("Sie:")
        if user_input:
            response = get_completion(user_input)
            chat_history.append({"role": "user", "message": user_input})
            chat_history.append({"role": "Jarvis", "message": response})
            save_chat_history(st.session_state['session_key'], chat_history)

        # Zeige den Chatverlauf
        for chat in chat_history:
            role = chat["role"]
            message = chat["message"]
            with st.chat_message(role):
                st.write(message)
    else:
        st.warning("Bitte erstellen Sie einen neuen Chat oder wählen Sie einen vorhandenen Chat aus.")

def load_chat_history(session_key):
    try:
        with open(os.path.join('chat_data', f'{session_key}_chat_history.json'), 'r') as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []
    return chat_history

def save_chat_history(session_key, chat_history):
    with open(os.path.join('chat_data', f'{session_key}_chat_history.json'), 'w') as f:
        json.dump(chat_history, f)

if __name__ == "__main__":
    app()

