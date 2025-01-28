import streamlit as st
import os
from groq import Groq

# Load API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY environment variable not set.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def generate_job_description(job_info):
    """
    Generate a job description using the Groq API.
    """
    try:
        # API call to generate job description
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an HR Assistant. You will generate a structured job description based on the provided information."
                },
                {
                    "role": "user",
                    "content": f"Generate a job description based on the following information: {job_info}.Ensure the language is formal and concise. Include industry-specific terminology where appropriate."
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

        # Log the raw response content for debugging
        st.text("Raw response content:")
        st.text(response_content)

        # Remove triple backticks if present
        response_content = response_content.strip("```")

        return response_content
    except Exception as e:
        st.error(f"Error generating job description: {e}")
        return None


if __name__ == "__main__":
    import sys
    job_info = sys.argv[1]
    job_description = generate_job_description(job_info)
    print(job_description)