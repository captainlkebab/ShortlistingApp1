import streamlit as st
import pandas as pd
import subprocess
import os
from groq import Groq
import json

# API-Key und Client initialisieren
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Streamlit App Header
st.title("Welcome to the Shortlisting App")

st.markdown("""
Through this application, your organization can streamline the hiring process for any open position. 
Simply import candidate resumes in CSV format and upload them here.
By providing a Job Description, our system evaluates the candidates and outputs the top 10 for further interviews.
""")

# Job Description Input
st.subheader("Job Description")
job_description = st.text_area("Insert the Job Description here:", height=300)

def analyze_job_description(job_description):
    """Analyzes the provided Job Description using Groq."""
    structure_template = """{
      "jobTitle": "",
      "company": "",
      "location": "",
      "keyResponsibilities": ["", "", ""],
      "requiredSkills": ["", "", ""],
      "preferredQualifications": ["", "", ""]
    }"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an HR Assistant. You will analyze Job Descriptions for the necessary skills, responsibilities, and qualifications needed for the position."
                },
                {
                    "role": "user",
                    "content": f"Analyze the following Job Description: {job_description} and extract the necessary details using this structure: {structure_template}. DO NOT INVENT THINGS!"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        response_content = "".join([chunk.choices[0].delta.content or "" for chunk in completion])
        
        # Versuche, JSON zu parsen
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_response": response_content}

    except Exception as e:
        return {"error": str(e)}

if st.button("Save and Analyze Job Description"):
    if job_description.strip():
        analysis_result = analyze_job_description(job_description)
        if "error" not in analysis_result:
            st.success("Job description successfully analyzed!")
            st.subheader("Analyzer Output:")
            st.json(analysis_result)  # Zeige das JSON-Ergebnis direkt an
        else:
            st.error("Error analyzing Job Description:")
            st.text(analysis_result.get("raw_response", "No response available."))
    else:
        st.error("The Job Description field cannot be empty!")

# CSV Upload
st.subheader("CSV Upload")
resume_list = st.file_uploader("Upload candidate resumes in CSV format:", type=["csv"])

def process_csv_file(csv_file):
    """Laden und Verarbeiten der CSV-Datei."""
    try:
        df = pd.read_csv(csv_file)
        st.success("CSV file successfully uploaded!")
        st.dataframe(df.head())  # Zeige die ersten Zeilen der Datei an
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

if resume_list:
    df = process_csv_file(resume_list)

# CSV Processing with bestFit.py
if st.button("Find the best candidates for the position."):
    if resume_list:
        csv_file_path = "uploaded_file.csv"
        with open(csv_file_path, "wb") as file:
            file.write(resume_list.getbuffer())

        try:
            # Führe das Skript aus
            result = subprocess.run(
                ["python", "bestFit.py", csv_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            st.subheader("Output from bestFit.py:")
            st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error(f"Error running bestFit.py: {e.stderr}")
    else:
        st.error("Please upload a CSV file before processing!")
