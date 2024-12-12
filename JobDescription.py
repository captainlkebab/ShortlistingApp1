from groq import Groq
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY,  # Use the GROQ_API_KEY variable directly
)


def load_job_description(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def analyze_job_description(job_description):
    # JSON-Template für den Output
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


# Jobbeschreibung laden (wenn gewünscht)
job_description = load_job_description("Job.txt")  # Anpassen, falls erforderlich

# Beispiel-Aufruf
if __name__ == "__main__":
    output = analyze_job_description(job_description)
    print(json.dumps(output, indent=4, ensure_ascii=False))
