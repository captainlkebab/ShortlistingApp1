import requests
import json
import os

# Globale Konfigurationen
TOGETHER_API_KEY = '0d0196f9b88ed8acff24e16e3c58e21a57f085bffe081451d85ad19ff4a97b12'
BASE_URL = "https://api.together.xyz/v1"

# Strukturvorlage für die Extraktion
structure_template = """{
  "jobTitle": "", 
  "company": "",
  "location": "",
  "keyResponsibilities": [
    "", // Key responsibility 1
    "", // Key responsibility 2
    ""  // Key responsibility 3
  ],
  "requiredSkills": [
    "", // Skill 1
    "", // Skill 2
    ""  // Skill 3
  ],
  "preferredQualifications": [
    "", // Qualification 1
    "", // Qualification 2
    ""  // Qualification 3
  ],
  "jobSummary": ""
}
"""

def load_job_description(file_path):
    """
    Lädt die Jobbeschreibung aus einer Datei.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        if not content:
            raise ValueError("The job description file is empty.")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

def analyze_job_description(api_key, job_description, structure):
    """
    Analysiert die Jobbeschreibung mithilfe der Together-API.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an HR Assistant. You will analyze Job Descriptions for the necessary "
                    "skills, responsibilities, and qualifications needed for the position."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following Job Description: {job_description} and extract the "
                    f"necessary details using this structure: {structure}. DO NOT INVENT THINGS!"
                ),
            }
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Hebt HTTP-Fehler hervor
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

def main():
    # Dateipfad für die Jobbeschreibung
    file_path = "JobDescription.txt"

    try:
        # Jobbeschreibung laden
        job_description_content = load_job_description(file_path)

        # API-Aufruf
        response = analyze_job_description(TOGETHER_API_KEY, job_description_content, structure_template)

        # API-Antwort verarbeiten
        chat_completion = response.get('choices', [{}])[0].get('message', {}).get('content', "No content returned.")
        print("Extracted Job Details:")
        print(chat_completion)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
