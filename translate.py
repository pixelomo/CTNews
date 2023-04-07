import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_with_gpt(text, target_language="Japanese"):
    try:
        prompt = f"Translate the following English text to {target_language}:\n{text}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2048,  # Adjust the number of tokens based on the model limit
            n=1,
            stop=None,
            temperature=0.3,
        )

        translated_text = response.choices[0].text.strip()

        # Print debugging information
        print(f"Original Text: {text}")
        print(f"Translated Text: {translated_text}")

        return translated_text

    except Exception as e:
        print(f"Error during translation: {e}")
        return None
