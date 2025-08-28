from google import genai
import os

google_token = os.getenv("GOOGLE_TOKEN")
def message_bot(message, chunk_size=1000):
    client = genai.Client(api_key=google_token)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message
    )

    text = response.text

    messages = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    return messages

