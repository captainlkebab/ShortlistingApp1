from groq import Groq
import json
import os
from pydantic import BaseModel, Field
from typing import List, Optional
import textwrap
import pandas as pd

data=pd.read_csv("uploaded_file.csv")



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

# Extraction from CSV for specific person in Dataframe, not really best Fit checker
class ResumeExtractionScheme(BaseModel):
    job_title: str = Field(description="Current or most recent job title of the candidate")
    summary: str = Field(description="Brief summary or professional statement of the candidate") 
    skills: List[str] = Field(description="Key skills or expertise mentioned by the candidate") 
    experience: List[str] = Field(description="List of job roles and responsibilities the candidate has held with relevance to the position")
    education: List[str] = Field(description="Academic qualifications and degrees obtained by the candidate")
    certifications: Optional[List[str]] = Field(description="Certifications or training programs completed by the candidate")
    languages: Optional[List[str]] = Field(description="Languages spoken by the candidate")
    projects: Optional[List[str]] = Field(description="Projects or work experience relevant to the job applied for")
    achievements: Optional[List[str]] = Field(description="Notable accomplishments or awards the candidate has received")
    contact_email: str = Field(description="Email address of the candidate")
    category: str = Field(description="Category or type of job the candidate is applying for (e.g., HR, IT, Marketing)")


 # Convert the Pydantic schema to a JSON schema
json_schema = str(ResumeExtractionScheme.model_json_schema())

text = data

# Follow the schema provided below to extract the relevant details. Do not invent information that is not in the provided text. Output JSON only.


client = Groq(api_key=GROQ_API_KEY)
chat_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
   messages=[
        {"role": "system", 
         "content": "You are a Recruiter. Find the top 10 best candidates for the provided Job Description. Explain your reasoning. Output JSON only."},
        {"role": "user",
        "content": f"Extract information from the following resumes: {text}."
        },
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# Ausgabe sammeln
response_content = ""
for chunk in chat_completion:
    response_content += chunk.choices[0].delta.content or ""

output_path = "bestFit.json"
output_data = {"analysis_result": response_content,
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Analysis result saved to {output_path}")


# JSON-Daten direkt parsen
try:
    output_data = json.loads(response_content)  # Konvertiere JSON-String zu Python-Dictionary
    print("Analysis result:", output_data)  # Ergebnis direkt anzeigen
except json.JSONDecodeError as e:
    print(f"Fehler beim Laden der JSON-Daten: {e}")