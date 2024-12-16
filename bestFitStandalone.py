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

# Function to load job description from a file with automatic encoding detection
def load_job_description(file_path):
    """
    Reads the job description from the specified file and automatically detects the encoding.
    """
    try:
        # Automatically detect encoding and return the content as a string
        detected = from_path(file_path).best()
        if detected is None:
            raise RuntimeError("Failed to detect file encoding.")
        return str(detected)  # Convert the content into a string
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

# Load the job description from a file
job_description = load_job_description("Job.txt")  # Adjust the path if necessary

# Define the Pydantic schema to extract details from resumes
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

# Convert the data to a string representation of the resumes (assuming `text` refers to your DataFrame)
text = data

# Initialize the Groq API client and make a request to analyze the resumes and job description
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

# Collect the response
response_content = ""
for chunk in chat_completion:
    response_content += chunk.choices[0].delta.content or ""

# Save the results to a JSON file
output_path = "bestFit.json"
output_data = {"analysis_result": response_content, "job_description": job_description}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Analysis result saved to {output_path}")

# Try to parse the JSON response
try:
    output_data = json.loads(response_content)  # Convert JSON string to Python dictionary
    print("Analysis result:", output_data)  # Display the result
except json.JSONDecodeError as e:
    print(f"Error loading JSON data: {e}")  # If there is a JSON decoding error
