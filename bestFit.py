from groq import Groq
import json
import os
from pydantic import BaseModel, Field
from typing import List, Optional
import textwrap
import pandas as pd
from charset_normalizer import from_path

# Load data from a CSV file
data = pd.read_csv("uploaded_file.csv")

# Get the GROQ API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the client with the GROQ API key
client = Groq(
    api_key=GROQ_API_KEY,  # Use the GROQ_API_KEY variable directly
)

# Funktion zum Laden der JobAnalyzed.json Datei
def load_job_analyzed(file_path):
    """
    Liest die JobAnalyzed.json Datei und gibt den Inhalt als Python-Objekt zurück.
    """
    try:
        # Datei öffnen und JSON-Inhalt laden
        with open(file_path, "r", encoding="utf-8") as file:
            job_data = json.load(file)  # Die Datei wird als JSON geladen
        return job_data
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        raise RuntimeError(f"Error decoding JSON in the file '{file_path}'.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


# Load the job description from a file
job_analyzed = load_job_analyzed("JobAnalyzed.json")  # Adjust the path if necessary

text = data

structure_ranking = {"""
    rankedCandidates: 
    [
        {
            "name": "",
            "email": "",
            "rank":"",
            "keySkills": [],
            "experience": "",
            "reasoning": ""            
        }
    ]
"""}


# Initialize the Groq API client and make a request to analyze the resumes and job description
client = Groq(api_key=GROQ_API_KEY)
chat_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", 
         "content":
        f"You are a Recruiter. Find the top 5 best candidates for the provided Job Description analysis in {job_analyzed} and rank them. Use the {structure_ranking}. Output JSON only."},
        {"role": "user",
         "content": f"Extract information from the following resumes: {text}.Just output an JSON, we dont need any other text ! DO NOT INVENT THINGS."
        },
    ],
    temperature=0.5, 
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# Collect the response
response_content = ""
for chunk in chat_completion:
    response_content += chunk.choices[0].delta.content or ""

# Remove triple backticks and the json tag
response_content = response_content.strip("```json\n").strip("```")

# Attempt to parse the response content as JSON
try:
    analysis_result = json.loads(response_content)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}")
    analysis_result = {"error": "Failed to parse JSON", "raw_response": response_content}

# Save the results to a JSON file bestFit.json
output_path = "bestFit.json"
output_data = {"analysis_result": analysis_result}

try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"Analysis result saved to {output_path}")
except Exception as e:
    print(f"Error saving JSON data: {e}")



print(response_content)