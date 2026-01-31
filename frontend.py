import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/"

st.title("Campus Chatbot")

st.write("Ask a question about your timetable:")

# User input
user_query = st.text_input(
    label="Query",
    placeholder="When do we have Kriti Batra class on Monday?"
)

# Submit button
if st.button("Submit"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        payload = {
            "user_query": user_query
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("Response:")
                st.write(data.get("response"))

            elif response.status_code == 429:
                st.error("Rate limit exceeded. Try again later.")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Is FastAPI running?")
