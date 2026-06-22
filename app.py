import streamlit as st
import os
from dotenv import load_dotenv

# Load the secret API key from the .env file
load_dotenv()

from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response

# 1. Set up the web page title
st.title("🤖 Adaptive Support Agent")
st.write("I change my personality based on how you talk to me!")

# 2. Initialize the RAG Pipeline and Chat History in session state
if "rag_pipeline" not in st.session_state:
    # Initialize the database connection (this assumes you've already ingested documents)
    st.session_state.rag_pipeline = LocalRAGPipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle new user input
if prompt := st.chat_input("Type your support issue here..."):
    
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ADD THIS: Check for simple greetings
    greetings = ["hi", "hello", "hey", "help"]
    if prompt.strip().lower() in greetings:
        bot_reply = "Hello! I am your Support Agent. Please describe the issue you are facing in detail so I can assist you."
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
        st.stop() # Stops the rest of the code from running
    
    # Show user message on screen and save to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a loading spinner while the AI thinks
    with st.spinner("Analyzing persona and retrieving documents..."):
        
        # A. Classify the user's persona
        persona_data = classify_customer_persona(prompt)
        detected_persona = persona_data.get("persona", "Frustrated User")
        
        # B. Retrieve relevant documents from ChromaDB
        context_chunks = st.session_state.rag_pipeline.retrieve_context(prompt)
        
        # C. Generate the final response
        final_output = generate_adaptive_response(prompt, detected_persona, context_chunks)
        bot_reply = final_output["response"]

        # If escalated, you might want to show the JSON handoff data
        if final_output["escalated"]:
            st.warning("⚠️ Escalation Triggered!")
            with st.expander("View Handoff JSON"):
                st.json(final_output["handoff_summary"])

    # Show bot message on screen and save to history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(f"*(Detected Persona: {detected_persona})*\n\n" + bot_reply)