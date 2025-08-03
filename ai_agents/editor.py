from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def edit_content(content, human_feedback):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Content Editor. Apply the provided human feedback to improve the content's quality and alignment with requirements."},
                {"role": "user", "content": f"Content: {content[:1000]}\nFeedback: {human_feedback}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = f"Error editing content: {e}"
        print(error_message)
        return f"An error occurred while editing the content. Please try again later. Details: {e}"