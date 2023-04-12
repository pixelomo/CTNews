import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_with_gpt(text, target_language="Japanese"):
    try:
        briefing = (
            "あなたはプロの新聞記者兼編集者であり、世界的なニュースメディア「コインテレグラフ」の日本語版である「コインテレグラフジャパン」で日本人向けに記事をかいています。"
            "今から仮想通貨に関する英文のニュース記事を、読みやすい日本語記事に翻訳編集してください。\n"
            "・全体的に、日本経済新聞ぽい文体にしてください。\n"
            "・ですます調ではなく、である調で翻訳すること\n"
            "・英文の固有名詞や人名はカタカナ表記に直すこと\n"
            "・第一段落にくる最初の主語について、同段落の最後に簡単な定義をいれること。\n"
            "・第二段落で同記事の理解に必要となる言葉があれば、簡単な解説か定義をいれること。\n"
            "・人名がでてきたときは初回は氏をつける。二回目以降は苗字だけにして氏をつける。\n"
            "・ドル単位で表記されているUS$30,000のような数字は、以下のような形式に変換すること\n"
            "3万ドル(約X円)\n"
            "X＝現在のドル円為替レートで変換し表記\n"
            "・CRYPTOを暗号資産でなく仮想通貨と翻訳すること\n"
            "・ツイッターからの引用も、かぎかっこの中にいれてしっかり訳してください\n"
            "・かぎかっこの前には句読点や「、」はいれない。\n"
            "・記事の一番最初に、新聞の見出しのようなタイトルをつけること\n"
            "・タイトルは簡潔に書くこと\n"
            "・直訳ではなく、新聞記事としての文体にすること\n"
            "・一文の長さはなるべく100文字以内におさめる。\n"
            "・述べている、ではなく、のべている、と書く。\n"
            "・述べている、ではなく、という。、としてもよい。\n"
            "・本日ではなく、今日と訳する。\n"
            "・である、でなく、だ、を優先して使ってください。\n"
            "・STABLECOINは安定コインではなく、ステーブルコインと訳す\n"
            "・鍵括弧は全角でなく半角にしてください。\n"
            "・最後に「翻訳・編集　コインテレグラフジャパン」と記載してください。\n"
            "以下の記事を上記の条件を守りながら和訳してください。\n"
        )
        prompt = f"Translate the following English text to {target_language}:\n{text}"
        print("Text to translate:", text)
        print("Target language:", target_language)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,
            temperature=0.2,
            n=1,
        )

        print(response)

        translated_text = response.choices[0].message.content.strip()  # Update this line
        # Add additional print statements for debugging
        print("Response object:", response)
        print("Choices object:", response.choices)
        print("Choice object:", response.choices[0])
        print("Content attribute:", response.choices[0].message.content)

        # Print debugging information
        print(f"Original Text: {text}")
        print(f"Translated Text: {translated_text}")

        return translated_text

    # except Exception as e:
    #     print(f"Error during API request: {e}")
    #     return None

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None

# Example usage
if __name__ == "__main__":
    text = "This is an example text to be translated."
    translated_text = translate_with_gpt(text)
    print(f"Final translated text: {translated_text}")
