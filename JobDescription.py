import os
import json
from groq import Groq

# Load API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY environment variable not set.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def analyze_job_description(job_description):
    """
    Analyze the job description using the Groq API.
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

    try:
        # API call to analyze job description
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an HR Assistant. You will analyze Job Descriptions for the necessary skills, responsibilities, and qualifications needed for the position."
                },
                {
                    "role": "user",
                    "content": f"Analyze the following Job Description: {job_description} and extract the necessary details using this structure: {structure_template}. Write in bullet points. Just output a JSON, we don't need any other text! DO NOT INVENT THINGS!"
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Collect the output
        response_content = ""
        for chunk in completion:
            response_content += chunk.choices[0].delta.content or ""

        # Remove triple backticks if present
        response_content = response_content.strip("```")

        return response_content
    except Exception as e:
        return f"Error analyzing job description: {e}"

if __name__ == "__main__":
    import sys
    job_description = sys.argv[1]
    analysis_result = analyze_job_description(job_description)
    print(analysis_result)


# Save the analysis result to JobAnalyzed.json
try:
    with open("JobAnalyzed.json", "w", encoding="utf-8") as file:
        json.dump(json.loads(analysis_result), file, indent=4)
    print("Analysis result saved to JobAnalyzed.json")
except json.JSONDecodeError:
    print("Error: Failed to parse JSON response")
    print(analysis_result)
except Exception as e:
    print(f"Error saving analysis result: {e}")