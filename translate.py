import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_with_gpt4(text, model="gpt-3.5-turbo"):
    try:
        response = openai.Chat.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates English text to Japanese."},
                {"role": "user", "content": f"Translate the following English text to Japanese: {text}"}
            ],
            max_tokens=2048,  # Adjust the number of tokens based on the model limit
            temperature=0.3,
        )

        # Check if the response is valid and contains the expected fields
        if response and 'choices' in response and len(response.choices) > 0 and 'message' in response.choices[0] and 'content' in response.choices[0].message:
            translation = response.choices[0].message['content'].strip()

            # Print debugging information
            print(f"Original Text: {text}")
            print(f"Translated Text: {translation}")

            return translation
        else:
            print("Invalid response from the translation API:")
            print(response)
            return None

    except Exception as e:
        print(f"Error during translation: {e}")
        return None
