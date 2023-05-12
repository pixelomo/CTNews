# -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.configuration.timeout = 900

def translate_with_gpt(text, translated_title, max_retries=3, wait_time=60):
    retries = 0
    print('translating...')
    briefing = (
        "あなたはプロの新聞記者兼編集者であり、世界的なニュースメディア「コインテレグラフ」の日本語版である「コインテレグラフジャパン」で日本人向けに記事をかいています。"
        "今から仮想通貨に関する英文のニュース記事を、読みやすい日本語記事に翻訳編集してください。\n\n"
        "・全体的に、日本経済新聞ぽい文体にしてください。\n"
        "・ですます調ではなく、である調で翻訳すること\n"
        "・英文の固有名詞や人名はカタカナ表記に直すこと\n"
        "・人名がでてきたときは初回は氏をつける。二回目以降は苗字だけにして氏をつける。\n"
        "・ドル単位で表記されているUS$30,000のような数字は、以下のような形式に変換すること\n\n"
        "3万ドル(約X円)\n"
        "X＝現在のドル円為替レートで変換し表記\n\n"
        "・CRYPTOを暗号資産でなく仮想通貨と翻訳すること\n"
        "・ツイッターからの引用も、かぎかっこの中にいれてしっかり訳してください\n"
        "・かぎかっこの前には句読点や、はいれない。\n"
        "・直訳ではなく、新聞記事としての文体にすること\n"
        "・一文の長さはなるべく90文字以内におさめる。\n"
        "・述という漢字は「のべる」という言葉においては使わないこと\n"
        "・述べている、ではなく、だとという。、としてもよい。\n"
        "・本日ではなく、今日と訳する。\n"
        "・である、でなく、だ、を優先して使ってください。\n"
        "・であるという語尾をなるべく使わないようにしてください\n"
        "・のべた、を一度つかったら、そのあとは、とした、と語った、など違った表現の語尾にしてください。\n"
        "・80,321等の数字は8万321と変換する\n"
        "・80,321等の数字は80321とし、,を入れない\n"
        "・ETHはETHとそのまま表記してください\n"
        "・翻訳文は、少なくとも原文と同じ長さにする必要があります。\n"
        "・最後に「翻訳・編集　コインテレグラフジャパン」と記載してください。\n"
        "そして以下の記事を上記の条件を守りながら和訳してください。\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": text},
            ],
            max_tokens=5450,
            temperature=0.7,
            top_p=0.9,
            request_timeout=900,
            n=1,
        )

        translated_text = response.choices[0].message.content.strip()
        print("chunk: "+translated_text)

        return translated_text

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")

        if retries < max_retries - 1:
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retries += 1
            print(f"Retry {retries}/{max_retries}")

        else:
            print(f"Failed after {max_retries} retries. Exiting.")
            raise
        # return None

def translate_title_with_gpt(text, target_language="Japanese"):
    briefing = (
        "あなたはプロの新聞記者兼編集者であり、世界的なニュースメディア「コインテレグラフ」の日本語版である「コインテレグラフジャパン」で日本人向けに記事をかいています。"
        "今から仮想通貨に関する英文のニュース記事を、読みやすい日本語記事に翻訳編集してください。\n\n"
        "・全体的に、日本経済新聞ぽい文体にしてください。\n"
        "・ですます調ではなく、である調で翻訳すること\n"
        "・英文の固有名詞や人名はカタカナ表記に直すこと\n"
        "・人名がでてきたときは初回は氏をつける。二回目以降は苗字だけにして氏をつける。\n"
        "・ドル単位で表記されているUS$30,000のような数字は、以下のような形式に変換すること\n\n"
        "3万ドル(約X円)\n"
        "X＝現在のドル円為替レートで変換し表記\n\n"
        "・CRYPTOを暗号資産でなく仮想通貨と翻訳すること\n"
        "・ツイッターからの引用も、かぎかっこの中にいれてしっかり訳してください\n"
        "・かぎかっこの前には句読点や、はいれない。\n"
        "・直訳ではなく、新聞記事としての文体にすること\n"
        "・一文の長さはなるべく90文字以内におさめる。\n"
        "・述という漢字は「のべる」という言葉においては使わないこと\n"
        "・述べている、ではなく、だとという。、としてもよい。\n"
        "・本日ではなく、今日と訳する。\n"
        "・である、でなく、だ、を優先して使ってください。\n"
        "・であるという語尾をなるべく使わないようにしてください\n"
        "・のべた、を一度つかったら、そのあとは、とした、と語った、など違った表現の語尾にしてください。\n"
        "・80,321等の数字は8万321と変換する\n"
        "・80,321等の数字は80321とし、,を入れない\n"
        "・ETHはETHとそのまま表記してください\n"
        "そこで、上記の条件を守りながら、以下のタイトルを日本語に翻訳してください。\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": text},
            ],
            max_tokens=min(50, len(text)),
            temperature=0.9,
            n=1,
        )

        # print(response)

        translated_text = response.choices[0].message.content.strip()  # Update this line

        # Print debugging information
        # print(f"Original Title: {text}")
        # print(f"Translated Title: {translated_text}")

        return translated_text

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None


if __name__ == "__main__":
    text = "Bitcoin ordinals — also known as Bitcoin NFTs — have made their way into the limelight of the Web3 space, as more marketplaces continue to adopt and offer digital assets. On May 9, the cryptocurrency exchange Binance announced that it will support Bitcoin ordinals on its NFT marketplace in late May. The development will expand Binance’s multichain NFT ecosystem to include the Bitcoin network. Previously the Binance NFT market integrated with other decentralized networks, including BNB Chain, Ethereum and Polygon. Mayur Kamat, the head of product at Binance, commented on broadening the offerings in the marketplace and Bitcoin’s (BTC) crypto legacy: “Bitcoin is the OG of crypto.”The update allows Binance users to purchase and trade Bitcoin ordinals from existing Binance accounts. According to the announcement, the update will also include royalty support and “additional revenue generating opportunities” for those creating Bitcoin ordinals.Related: Bitcoin metrics to the moon: ATH for hash rate, daily transactions and OrdinalsPrior to Binance’s announcement, the cryptocurrency exchange OKX similarly announced in late April that it was bringing Bitcoin ordinals to its marketplace and wallet ecosystem. Initially, OKX users could view and store ordinals using their accounts, with the option to mint ordinals being hinted at in the future, according to Haider Rafique, the chief marketing officer at OKX.The Bitcoin NFTs are also available on marketplaces such as Magic Eden, which integrated the feature back in March. Ordinals reach 3 million inscriptions. Source: DuneAccording to recent data, inscriptions of Bitcoin ordinals have been on the rise in recent months. On April 2, Bitcoin ordinals reached 58,179 inscriptions — up 83.5% from the previous month. However, on May 1, the total number of Bitcoin ordinal inscriptions skyrocketed to exceed 3 million. Nonetheless, they remain a controversial topic within the crypto community, with Bitcoin maximalists criticizing them for deviating from Bitcoin’s original peer-to-peer ethos.Magazine: ZK-rollups are ‘the endgame’ for scaling blockchains: Polygon Miden founder"
    translated_text = translate_with_gpt(text, "BTCが不安定な週末に3％下落したため、次にこれらのビットコインの価格水準に注目する。")
    print(f"Final translated text: {translated_text}")
