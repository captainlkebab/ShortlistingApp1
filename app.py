import streamlit as st 
import pandas as pd 
import numpy as np  
import subprocess


st.title("Welcome to this shortlisting app")

st.markdown("""Through this application your organization can streamline the hiring process for any open position. 
Simply import the candidate Resume CSV and upload it here.
by providing the Job Descriptions our Evaluation system can output the top 10 best candidates for the position to invite them to further interviews.""")

st.subheader("Job Description")

job_description = st.text_area("Insert the Job Description for the desired job here.",height=300)

# Button, um den Text zu speichern
if st.button("Save Job description"):
    # Speichern des Textes in einer Datei
    if job_description.strip():  # Überprüfen, ob der Text nicht leer ist
        with open("JobDescription.txt", "w", encoding="utf-8") as file:
            file.write(job_description)
        st.success("Jobbeschreibung wurde erfolgreich gespeichert!")
    else:
        st.error("Das Eingabefeld darf nicht leer sein!")

if job_description:
    st.write("Jobbeschreibung wurde erfolgreich gespeichert in JobDescription.txt")
else: 
    st.write("Keine Jobbeschreibung eingegeben")



# CSV-Upload
st.subheader("CSV-Datei upload")
uploaded_file = st.file_uploader("Upload the CSV file with the resumes here:", type=["csv"])

if uploaded_file:
    try:
        # CSV in ein DataFrame laden
        df = pd.read_csv(uploaded_file)
        st.success("CSV-Datei wurde erfolgreich hochgeladen!")
        
        # Vorschau der ersten Zeilen der Datei anzeigen
        st.dataframe(df.head())
        
        # Button für die Verarbeitung mit bestFit.py
        if st.button("Mit bestFit.py verarbeiten"):
            # Speichere die hochgeladene Datei lokal
            csv_file_path = "uploaded_file.csv"
            with open(csv_file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())
            
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

