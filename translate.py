import openai
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_with_gpt4(text, model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        engine=model,
        prompt=f"Translate the following English text to Japanese:\n{text}\nTranslation:",
        max_tokens=4000,  # Adjust the number of tokens based on the model limit
        n=1,
        stop=None,
        temperature=0.3,
    )

    return response.choices[0].text.strip()
