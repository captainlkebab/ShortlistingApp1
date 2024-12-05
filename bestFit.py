# %%
from openai import OpenAI
import json
from pydantic import BaseModel, Field
from typing import List, Optional
import textwrap
import pandas as pd


data=pd.read_csv("uploaded_file.csv")

# %%
# Setup OpenAI client with custom API key and base URL
TOGETHER_API_KEY='0d0196f9b88ed8acff24e16e3c58e21a57f085bffe081451d85ad19ff4a97b12'

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=TOGETHER_API_KEY
)

# %%
# put scores in

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

# %%
text = data.loc[3,'Resume']
# category =data.loc[3,'Category'] # not used yet, cant seem to work it out
#email = data.loc[3, 'Email'] # not used yet, cant seem to work it out

# Call the LLM to output attributes
chat_completion = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[
        {"role": "system", 
         "content": "You are a Recruiter. Follow the schema provided below to extract the relevant details. Do not invent information that is not in the provided text. Output JSON only."},
        {"role": "user",
        "content": f"Extract information from the following resumes: {text}\nUse the following JSON schema: {json_schema}"
        },
    ],
)

output = chat_completion.choices[0].message.content
print(output)
# Ergänze die weiteren Informationen (Category, Email) im JSON-Output
#output_json = json.loads(output)
#output_json['category'] = category  # not used yet, cant seem to work it out
# output_json['email'] = email  # # not used yet, cant seem to work it out
print(textwrap.fill(output, width=100))





# Speichere die Ergebnisse in einer JSON-Datei
with open('Output.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

# %%



