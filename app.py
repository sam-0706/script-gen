import streamlit as st
import json
from openai import OpenAI


# Load JSON structure from file
def load_json():
    with open("x.json", "r") as file:
        return json.load(file)


json_structure = load_json()

# Secure OpenAI API key using Streamlit secrets
api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=api_key)

# Password authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Enter Password", type="password")
    if password == "test":
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.stop()

st.title("AI-Powered Script Generator")

# Dropdown for Year Selection
year = st.selectbox("Select Year", list(json_structure.keys()))

# Dynamic Semester Selection
semester_options = list(json_structure[year].keys())
semester = st.selectbox("Select Semester", semester_options)

# Dynamic Subject Selection
subject_options = list(json_structure[year][semester].keys())
subject = st.selectbox("Select Subject", subject_options) if subject_options else None

# Dynamic Unit Selection
unit_options = list(json_structure[year][semester][subject].keys()) if subject else []
unit = st.selectbox("Select Unit", unit_options) if unit_options else None

# Generate script using OpenAI
if st.button("Generate Script"):
    if year and semester and subject and unit:
        unit_name = unit  # Store the unit key (e.g., "Unit 3")
        unit_content = json_structure[year][semester][subject][unit]  # Get actual unit value

        user_prompt = (
            f"Generate a detailed script for **{unit_name}: {unit_content}** "
            f"in {subject} under {semester} of {year}. "
            f"Ensure the response is well-structured with markdown formatting.\n\n"
            f"Topics Covered: {unit_content}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            store=True,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # Extract the content properly
        script_text = response.choices[0].message.content
        # Display the script with proper formatting
        st.subheader(f"Generated Script for: {unit_name}")
        st.markdown(f"## {unit_name} - {subject}")
        st.markdown(f"**Topics Covered:** {unit_content}")
        st.markdown(script_text, unsafe_allow_html=True)

    else:
        st.error("Please select all fields before generating the script.")
