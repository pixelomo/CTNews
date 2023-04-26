# -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

brief = "あなたはプロの新聞記者兼編集者であり、世界的なニュースメディア「コインテレグラフ」の日本語版である「コインテレグラフジャパン」で日本人向けに記事をかいています。今から仮想通貨に関する英文のニュース記事を、読みやすい日本語記事に翻訳編集してください。全体的に、日本経済新聞ぽい文体にしてください。ですます調ではなく、である調で翻訳すること. 英文の固有名詞や人名はカタカナ表記に直すこと. 第一段落にくる最初の主語について、同段落の最後に簡単な定義をいれること。第二段落で同記事の理解に必要となる言葉があれば、簡単な解説か定義をいれること。人名がでてきたときは初回は氏をつける。二回目以降は苗字だけにして氏をつける。ドル単位で表記されているUS$30,000のような数字は、以下のような形式に変換すること 3万ドル(約X円), X＝現在のドル円為替レートで変換し表記. CRYPTOを暗号資産でなく仮想通貨と翻訳すること. ツイッターからの引用も、かぎかっこの中にいれてしっかり訳してください. かぎかっこの前には句読点や「、」はいれない。・かぎかっこや（）は半角でいれてください・記事の一番最初に、新聞の見出しのようなタイトルをつけること・タイトルは簡潔に書くこと. 新聞記事としての文体にすること・一文の長さはなるべく100文字以内におさめる。・述べる、述べている、述べた、という表現を使う際、漢字の述を使わず、ひらがなで書く。例えばのべた、のべている、のべる、の様に。・述べている、ではなく、という。、としてもよい。・本日ではなく、今日と訳する。・である、でなく、だ、を優先して使ってください。・のべた、を一度つかったら、そのあとは、とした、と語った、など違った表現の語尾にしてください。・STABLECOINは安定コインではなく、ステーブルコインと訳す・鍵括弧は全角でなく半角にしてください。・80,321等の数字は80321とし、,を入れない・数字には三桁ごとに,をいれないでください・ETHはETHとそのまま表記してください・英語原文にあるRelated: は削除してください・英語原文にあるMagazine: は削除してください・最後に文章の内容を要約し、かつ、新聞の見出しのようにわかりやすい標題をつけてください. そして以下の記事を上記の条件を守りながら和訳してください。"

def translate_with_gpt(text, target_language="Japanese"):
    try:
        briefing = brief
        prompt = f"Translate the following text to {target_language}:\n{text}"
        print("Text to translate:", text)
        print("Target language:", target_language)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": prompt},
            ],
            max_tokens=5650,
            temperature=0.9,
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

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None

if __name__ == "__main__":
    text = brief + "OpenSea ‘insider trading’ trial kicked off in New York district court. The court case might have a decisive influence on the legal classification of NFTs. On April 24, the Southern district court of New York held the first jury hearing on the case against former OpenSea product manager Nathaniel Chastain, who’s being accused of insider trading with nonfungible tokens (NFTs). The allegations were filed by the United States Manhattan Attorney’s Office on May 31, 2022. Chastain is being indicted on two counts — wire fraud and money laundering. On the first count, the former employee of the largest NFT market presumably used his insider knowledge to secretly buy 45 NFTs shortly before their listing to sell them with a profit immediately afterward. The filing cites several examples of misconduct, such as the case with NFT “The Brawl 2.” In August 2021, through anonymous accounts, Chastain allegedly bought four of them “minutes before” they got featured on OpenSea and sold them within hours with 100% profit. In October 2022, Chastain’s lawyers unsuccessfully filed a motion to remove “insider trading” references from his charges. Chastain argued the use of “insider trading” to describe his alleged actions is “inflammatory,” as “insider trading” only applies to securities and not to NFTs. Prosecutors responded, noting that the allegation of “insider trading” can be used to reference multiple types of fraud in which someone with non-public knowledge uses it to trade assets. Related: SEC reaches ‘agreement in principle’ to resolve insider trading case of Coinbase product manager. Advertisement AI-Powered Indicator Sent Out 204 Winning Alerts in 2022. Click For Details >>>. As the term “insider trading” had previously not been used in reference to cryptocurrencies or NFTs before Chastain’s charges, the outcome of the trial, which is expected to last several weeks, might have a major influence on the legal classification of NFTs. In 2022, former U.S. Securities and Exchange Commission lawyer Alma Angotti predicted that the case might see NFTs labeled as securities, as they could be considered one under the Howey test. In a recent commentary to Reuters, another former employee of the SEC, Philip Moustakis, expressed a similar concern:“If this case sticks, there is precedent that insider trading theory can be applied to any asset class.” In another important recent court case, crypto exchange Coinbase supported a motion to dismiss the case on insider trading against the brother of the platform’s former product manager, who’s been allegedly using insider knowledge to trade cryptocurrencies. Coinbase argues that the SEC had no jurisdiction to file a lawsuit, given the tokens in question do not pass the Howey test. Magazine: Best and worst countries for crypto taxes — Plus crypto tax tips"
    translated_text = translate_with_gpt(text)
    print(f"Final translated text: {translated_text}")
