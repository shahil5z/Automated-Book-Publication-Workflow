from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def review_content(content):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Content Reviewer. Enhance the following content for clarity, coherence, and professional tone."},
                {"role": "user", "content": content[:1000]}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error reviewing content: {e}"
        print(error_message)
        return f"An error occurred while reviewing the content. Please try again later. Details: {e}"