from groq import Groq
import json
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY, # Use the GROQ_API_KEY variable directly
)


def load_job_description(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

job_description = load_job_description("Job.txt")  # Adjust the path if necessary
    
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
  "
}
"""

from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "\"You are an HR Assistant. You will analyze Job Descriptions for the necessary skills, responsibilities, and qualifications needed for the position.\""
        },
        {
            "role": "user",
            "content": f"\"Analyze the following Job Description:{job_description} and extract the necessary details using this structure: {structure_template}. DO NOT INVENT THINGS!\""
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

output_path = "JobAnalysis.json"
output_data = {"analysis_result": response_content,
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Analysis result saved to {output_path}")
