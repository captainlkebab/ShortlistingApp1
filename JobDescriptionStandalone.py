from groq import Groq
import json
import os
from charset_normalizer import from_path

# API-Key aus Umgebungsvariablen laden
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq-Client initialisieren
client = Groq(api_key=GROQ_API_KEY)


def load_job_description(file_path):
    """
    Liest die Jobbeschreibung aus der angegebenen Datei ein und erkennt die Kodierung automatisch.
    """
    try:
        # Kodierung automatisch erkennen und Inhalt als String zurückgeben
        detected = from_path(file_path).best()
        if detected is None:
            raise RuntimeError("Failed to detect file encoding.")
        return str(detected)  # Konvertiert den Inhalt in einen String
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def analyze_job_description(job_description):
    """
    Analysiert die Jobbeschreibung mithilfe der Groq-API.
    """
    structure_template = """{
      "jobTitle": "",
      "company": "",
      "location": "",
      "keyResponsibilities": [
        "", "", ""
      ],
      "requiredSkills": [
        "", "", ""
      ],
      "preferredQualifications": [
        "", "", ""
      ]
    }"""

    # API-Aufruf zur Analyse
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
        stream=True,
        stop=None,
    )

    # Ausgabe sammeln
    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    # JSON-Daten parsen
    try:
        analysis_result = json.loads(response_content)
        return analysis_result
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_response": response_content}


def save_to_json_file(data, output_file_path):
    """
    Speichert die Analyseergebnisse in einer JSON-Datei.
    """
    try:
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Output successfully saved to {output_file_path}")
    except Exception as e:
        raise RuntimeError(f"Error saving JSON file: {e}")


if __name__ == "__main__":
    # Dateipfade
    input_file = "Job.txt"
    output_file = "JobAnalyzed.json"

    try:
        # Jobbeschreibung laden
        job_description = load_job_description(input_file)

        # Jobbeschreibung analysieren
        analysis_result = analyze_job_description(job_description)

        # Analyseergebnisse speichern
        save_to_json_file(analysis_result, output_file)

    except Exception as e:
        print(f"Error: {e}")
