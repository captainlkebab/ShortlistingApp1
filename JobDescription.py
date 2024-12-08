import requests
import json
import os
import openai
import subprocess
import threading
from IPython.display import clear_output, HTML
from tqdm import tqdm
import ollama

JobDescription = "JobDescription.txt"


structure_template = """{
  "jobTitle": "", // The title or role of the job
  "company": "", // Name of the company
  "location": "", // Job location
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
  "jobSummary": "", // A short description summarizing the role
  "applicationLink": "" // Link to apply for the job
}



"""

# Set up the Ollama chat call
response = ollama.chat(
    model='qwen2.5',
    messages=[
        {
            "role": "system",
            "content": "You are an HR Assistant. You will analyze Job Descriptions for the necessary Skills the future employee needs to offer.",
        },
        {
            "role": "user",
            "content": f"Analyze the following Job Description{JobDescription} and extract the necessary skills to perform successfully in the position.. Use this structure to guide the extraction: {structure_template}. DO NOT INVENT THINGS! STICK TO THE TRANSCRIPT!"
        }
    ]
)

# Extract and print the response
chat_completion = response['message']['content']
print(chat_completion)