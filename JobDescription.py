import requests
import json
import os
import torch
from transformers import pipeline
from huggingface_hub import login

model_id = "meta-llama/Llama-3.3-70B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Jobbeschreibung laden
file_path = "JobDescription.txt"
def load_job_description(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")
    

job_description = load_job_description(file_path)

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
  "
}
"""

messages = [
    {"role": "system", "content": "You are an HR Assistant. You will analyze Job Descriptions for the necessary skills, responsibilities, and qualifications needed for the position."},
    {"role": "user", "content": f"Analyze the following Job Description: {job_description} and extract the "
                    f"necessary details using this structure: {structure_template}. DO NOT INVENT THINGS!"},
]
outputs = pipe(
    messages,
    max_new_tokens=256,
)
print(outputs[0]["generated_text"][-1])