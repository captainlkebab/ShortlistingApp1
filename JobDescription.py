import requests
import json
import os
import openai
import subprocess
import threading
from IPython.display import clear_output, HTML
from tqdm import tqdm


with open ("JobDescription.txt", 'r') as file:
    job_description_content = file.read()
JobDescription = "JobDescription.txt"


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
  "jobSummary": "",
}



"""


# Set up the OpenAI chat call
response = openai.ChatCompletion.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an HR Assistant. You will analyze Job Descriptions for the necessary Skills the future employee needs to offer.",
        },
        {
            "role": "user",
            "content": f"Analyze the following Job Description: {job_description_content} and extract the necessary skills to perform successfully in the position. Use this structure to guide the extraction: {structure_template}. DO NOT INVENT THINGS!"
        }
    ]
)

# Extract and print the response
chat_completion = response['choices'][0]['message']['content']
print(chat_completion)