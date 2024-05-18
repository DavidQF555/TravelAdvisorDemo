from chains.information_extractor import Information_Extractor
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from chains.tagger import Tagger
from chains.summarizer import Summarizer
from utils.logger import logger

_ = load_dotenv(find_dotenv())  # read local .env file

st.title("Dest GPT - AI Agent that uses Trip Advisor API to answer questions about travel destinations")
logger.propagate = False
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(
    "I am a helpful travel destinations bot. Ask me anything about travel destinations!"
):
    try:
        tagger = Tagger(os.getenv("OPENAI_API_KEY"))
        information_extractor = Information_Extractor(os.getenv("OPENAI_API_KEY"))
        summarizer = Summarizer(os.getenv("OPENAI_API_KEY"))
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            st.markdown("Let me check that for you...")
        user_intent = tagger.extract_information(prompt)
        with st.chat_message("assistant"):
            st.markdown(
                f"Got it! You want to know about the {user_intent.name} and want to talk about the {user_intent.intent}."
            )
        information = information_extractor.get_information(user_intent)
        summary = summarizer.summarize(information, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(summary)
        st.session_state.messages.append({"role": "assistant", "content": summary})
    except Exception as e:
        logger.debug(f"Error: {e}")
        message = f"I was not able to process the request. I am a travel destinations bot and I can only answer questions about travel destinations."
        st.markdown(message)
        st.session_state.messages.append({"role": "assistant", "content": message})
