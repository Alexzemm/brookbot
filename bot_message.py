from google import genai

def message_bot(message, chunk_size=1000):
    client = genai.Client(api_key="AIzaSyBkd2kSANEaOUI-mWmoyYHkZz6KcAu5SnU")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message
    )

    text = response.text

    messages = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    return messages
