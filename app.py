import streamlit as st
import pandas as pd
import subprocess
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_id = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# **Streamlit App Header**
st.title("Welcome to the Shortlisting App")

st.markdown("""
Through this application, your organization can streamline the hiring process for any open position. 
Simply import candidate resumes in CSV format and upload them here.
By providing a Job Description, our system evaluates the candidates and outputs the top 10 for further interviews.
""")

# **Job Description Input**
st.subheader("Job Description")
job_description = st.text_area("Insert the Job Description here:", height=300)

def save_and_analyze_job_description(job_description):
    """Speichern und Analyse der Jobbeschreibung."""
    file_path = "JobDescription.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(job_description)
    
    # try:
    #     # JobDescription.py ausführen
    #     result = subprocess.run(
    #         ["python", "JobDescription.py", file_path],
    #         capture_output=True,
    #         text=True,
    #         check=True
    #     )
    #     return result.stdout
    # except subprocess.CalledProcessError as e:
    #     st.error(f"Error running JobDescription.py: {e.stderr}")
    #     return None

if st.button("Save and Analyze Job Description"):
    if job_description.strip():
        output = save_and_analyze_job_description(job_description)
        if output:
            st.success("Job description successfully analyzed!")
            st.subheader("Analyzer Output:")
            st.text(output)
    else:
        st.error("The Job Description field cannot be empty!")

# **CSV Upload**
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

# **CSV Processing with bestFit.py**
if st.button("Find the top 10 candidates for the position."):
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

