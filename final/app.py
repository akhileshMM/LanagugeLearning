import streamlit as st
from chatbot import LightweightSemanticLanguageLearningAssistant

# Initialize chatbot
assistant = LightweightSemanticLanguageLearningAssistant("train.en", "train.kn")

# Streamlit UI
st.title("Dhwani - Kannada Learning Assistant")
st.markdown("### Learn Kannada through engaging conversations!")

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your query...")

if user_input:
    # Append user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    response = assistant.generate_conversational_response(user_input)
    
    # Append assistant response to session state
    st.session_state["messages"].append({"role": "assistant", "content": response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
