from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_content(content):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Content Generator. Rewrite the following content in a professional style while preserving its core meaning."},
                {"role": "user", "content": content[:1000]}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error generating content: {e}"
        print(error_message)
        return f"An error occurred while generating the content. Please try again later. Details: {e}"