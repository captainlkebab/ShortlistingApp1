import streamlit as st
import pandas as pd
import subprocess
import os
from groq import Groq
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=GROQ_API_KEY)

# **Streamlit App Header**
st.title("Welcome to the Shortlisting App")

st.markdown("""
Through this application, your organization can streamline the hiring process for any open position. 
Simply import candidate resumes in CSV format and upload them here.
By providing a Job Description, our system evaluates the candidates and outputs the top 5 best candidates for further review.
""")


st.subheader("Job Description Builder")
ad_creator = st.text_area("Insert Details regarding the role you want to hire for. This includes: Company Name, Location, Role Name, Key Qualifications, etc.", height=100)


def save_user_input(input_text,filename):
    """Save user input to a JSON file."""
    data = {"input": input_text}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)


def create_job_description(job_ad):
    """Generate the Job Description using the Groq API."""
    try:
        # save user input into JSON
        save_user_input(job_ad, "user_input_jobAdBuilder.json")

        # JobAdBuilder.py ausführen
        result = subprocess.run(
            ["python", "JobAdBuilder.py", job_ad],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        st.error(f"Error running JobAdBuilder.py: {e.stderr}")
        return None
    
if st.button("Save and Build Job Description"):
    if ad_creator.strip():
        output = create_job_description(ad_creator)
        if output:
            st.success("Job description successfully built!")
            st.subheader("Builder Output:")
            adjusted_output = st.text_area("Adjust the Job Description if needed:", output, height= 500)
            if st.button("Save Adjusted Job Description"):
                with open("AdjustedJobDescription.json", "w") as file:
                    json.dump({"adjusted_output": adjusted_output}, file, indent=4)
                st.success("Adjusted Job Description saved successfully!")
    else:
        st.error("The Job Description field cannot be empty!")


# **Job Description Input**
st.subheader("Job Description Analyzer")
job_description = st.text_area("Insert the Job Description here:", height=500)


def save_and_analyze_job_description(job_description):
    """Analyze the Job Description using the Groq API."""
    try:
        # save user input
        save_user_input(job_description, "user_input_JobDescriptionAnalyzer.json")

        # JobDescription.py ausführen
        result = subprocess.run(
            ["python", "JobDescription.py", job_description],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        st.error(f"Error running JobDescription.py: {e.stderr}")
        return None


def display_analysis_result(analysis_result):
    """Display the analysis result a structured format."""
    st.markdown(f"**Job Title:** {analysis_result.get('jobTitle', '')}")
    st.markdown(f"**Company:** {analysis_result.get('company', '')}")
    st.markdown(f"**Location:** {analysis_result.get('location', '')}")
    st.markdown("**Key Responsibilities:**")
    for responsibility in analysis_result.get('keyResponsibilities', []):
        st.markdown(f"- {responsibility}")
    st.markdown("**Required Skills:**")
    for skill in analysis_result.get('requiredSkills', []):
        st.markdown(f"- {skill}")
    st.markdown("**Preferred Qualifications:**")
    for qualification in analysis_result.get('preferredQualifications', []):
        st.markdown(f"- {qualification}")


if st.button("Save and Analyze Job Description"):
    if job_description.strip():
        output = save_and_analyze_job_description(job_description)
        if output:
            st.success("Job description successfully analyzed!")
            st.subheader("Analyzer Output:")
            try:
                analysis_result = json.loads(output)
                display_analysis_result(analysis_result)
                #Save the analysis result to a JSON file for later use
                if os.path.exists("JobAnalyzed.json"):
                    with open("JobAnalyzed.json", "r") as file:
                        existing_data = json.load(file)
                else:
                    existing_data = []

                existing_data.append(analysis_result)

                with open("JobAnalyzed.json", "w") as file:
                    json.dump(existing_data, file, indent=4)

                adjusted_output = st.text_area("Adjust the Analyzed Job Description if needed:", json.dumps(analysis_result, indent=4), height= 500)
                if st.button("Save Adjusted Analyzed Job Description"):
                    if os.path.exists("AdjustedJobAnalyzed.json"):
                        with open("AdjustedJobAnalyzed.json", "r") as file:
                            existing_data = json.load(file)
                    else:
                        existing_adjusted_data = []

                    existing_adjusted_data.append({"adjusted_output": adjusted_output})

                    with open("AdjustedJobAnalyzed.json", "w") as file:
                        json.dump(existing_adjusted_data, file, indent=4)
                    st.success("Adjusted Analyzed Job Description saved!")
            except json.JSONDecodeError:
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
        st.dataframe(df.head())  # show first rows for checking
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

if resume_list:
    df = process_csv_file(resume_list)

# **CSV Processing with bestFit.py**
if st.button("Find the best candidates for the position."):
    if resume_list:
        csv_file_path = "uploaded_file.csv"
        with open(csv_file_path, "wb") as file:
            file.write(resume_list.getbuffer())
        
        try:
            # Führe das Skript aus
            result = subprocess.run(
                ["python", "BestFit.py", csv_file_path],
                capture_output=True,
                text=True,
                check=True
            )
            st.subheader("Output from bestFit.py:")
            try:
                analysis_result = json.loads(result.stdout)
                st.json(analysis_result)
            except json.JSONDecodeError:
                st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error(f"Error running bestFit.py: {e.stderr}")
    else:
        st.error("Please upload a CSV file before processing!")