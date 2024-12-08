import streamlit as st 
import pandas as pd 
import numpy as np  
import subprocess
import os
import threading


def start_ollama():
    os.environ['OLLAMA_HOST'] = '0.0.0.0:11434'
    os.environ['OLLAMA_ORIGINS'] = '*'
    subprocess.Popen(["ollama", "serve"])

ollama_thread = threading.Thread(target=start_ollama)
ollama_thread.start()

st.title("Welcome to this shortlisting app")

st.markdown("""Through this application your organization can streamline the hiring process for any open position. 
Simply import the candidate Resume CSV and upload it here.
by providing the Job Descriptions our Evaluation system can output the top 10 best candidates for the position to invite them to further interviews.""")

st.subheader("Job Description")

job_description = st.text_area("Insert the Job Description for the desired job here.",height=300)

if st.button("Save and Analyze Job Description"):
    if job_description.strip():  # Überprüfen, ob der Text nicht leer ist
        # Speichern der Jobbeschreibung
        file_path = "JobDescription.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(job_description)
        st.success("Job description successfully uploaded!")
        
# Run von JobDescription.py
        try:
            result = subprocess.run(
                ["python", "JobDescription.py", file_path],
                capture_output=True,
                text=True,
                check=True
            )
            st.subheader("Analyzer Output:")
            st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error(f"Error running JobDescription.py: {e.stderr}")
    else:
        st.error("The input field cannot be empty!")



# CSV-Upload
st.subheader("CSV-Datei upload")
resume_list = st.file_uploader("Upload the CSV file with the resumes here:", type=["csv"])

if resume_list:
    try:
        # CSV in ein DataFrame laden
        df = pd.read_csv(resume_list)
        st.success("CSV-Datei wurde erfolgreich hochgeladen!")
        
        # Vorschau der ersten Zeilen der Datei anzeigen
        st.dataframe(df.head())
        
        # Button für die Verarbeitung mit bestFit.py
        if st.button("Mit bestFit.py verarbeiten"):
            # Speichere die hochgeladene Datei lokal
            csv_file_path = "uploaded_file.csv"
            with open(csv_file_path, "wb") as file:
                file.write(resume_list.getbuffer())
            
            # Führe das bestFit-Skript aus
            try:
                result = subprocess.run(
                    ["python", "bestFit.py", csv_file_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Zeige die Ausgabe des Skripts in der App an
                st.subheader("Ausgabe von bestFit.py:")
                st.text(result.stdout)
            except subprocess.CalledProcessError as e:
                st.error(f"Fehler bei der Ausführung von bestFit.py: {e.stderr}")
    except Exception as e:
        st.error(f"Fehler beim Laden der CSV-Datei: {e}")

