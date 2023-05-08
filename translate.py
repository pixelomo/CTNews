# -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_with_gpt(text, translated_title, retries=3):
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
        "・英語原文にあるRelated: は削除してください\n"
        "・英語原文にあるMagazine: は削除してください\n"
        "・最後に「翻訳・編集　コインテレグラフジャパン」と記載してください。\n"
        "そして以下の記事を上記の条件を守りながら和訳してください。\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": f"Following our writing style and rules translate this article into Japanese: {text}"},
            ],
            max_tokens=5400,
            temperature=0.9,
            n=1,
        )

        print(response)
        translated_text = response.choices[0].message.content.strip()

        return translated_text

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None

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
        "・英語原文にあるRelated: は削除してください\n"
        "・英語原文にあるMagazine: は削除してください\n"
        "・最後に「翻訳・編集　コインテレグラフジャパン」と記載してください。\n"
        "そこで、上記の条件を守りながら、以下のタイトルを日本語に翻訳してください。\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": f"Following our writing style and rules translate this title into Japanese: {text}"},
            ],
            max_tokens=min(50, len(text)),
            temperature=0.9,
            n=1,
        )

        print(response)

        translated_text = response.choices[0].message.content.strip()  # Update this line

        # Print debugging information
        print(f"Original Title: {text}")
        print(f"Translated Title: {translated_text}")

        return translated_text

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None


if __name__ == "__main__":
    text = "Some swift down moves fail to make Bitcoin dislodge a familiar trading range, with one trader calling it “in limbo.“ Bitcoin saw fresh volatility on May 6 as low-liquidity weekend trading tested the mettle of its trading range. BTC/USD 1-hour candle chart (Bitstamp). Source: TradingView. Bitcoin “in limbo” despite volatility. Data from Cointelegraph Markets Pro and TradingView showed BTC/USD dropping by over $1,000, or 3%, in a matter of hours on the day. The largest cryptocurrency saw volatile conditions typical of weekend trading but could not exit a broader corridor in place for several weeks. Amid a lack of ammunition to either clear the $30,000 resistance or drop toward key trend lines near $25,000, BTC/USD frustrated market participants. “Bitcoin really is in limbo right now and doesn’t know what to do .. I am back out of a position and just waiting again for one side of this range to break to re enter,” popular trader Crypto Tony told Twitter followers. An accompanying chart showed potential targets in the event of a bearish breakdown. BTC/USD annotated chart. Source: Crypto Tony/Twitter. An additional analysis released earlier in the day repeated previous predictions of $32,000 coming into play should bullish momentum return. In separate coverage, fellow trader CryptoBullet described the day’s losses as “nothing special.” Advertisement The basic building blocks of DeFi and NFTs in one place - the ABCs of Crypto Report by Cointelegraph Research. “Final dip before the breakout,” part of the commentary argued, with a chart presenting BTC/USD in a narrowing wedge with a decision on exit trajectory due. BTC price bulls must clear $30,000. As ever, longer timeframes were a cause for more optimistic views. Related: Bitcoin trader eyes $63K BTC price for new Bollinger Bands ‘breakout’. Analyzing the weekly chart, analyst Gert van Lagen flagged the 200-week simple moving average (SMA) as the resistance line to clear next, with Bitcoin possibly completing a bullish inverse head and shoulders chart pattern. BTC/USD annotated chart. Source: Gert van Lagen/Twitter. Trader and investor CryptoAce highlighted a large weekly resistance zone for bulls to tackle. “Stay below and $24k is where price will be trading in some weeks imo,” part of an update on trading activity read on the day. Magazine: Unstablecoins: Depegging, bank runs and other risks loom. This article does not contain investment advice or recommendations. Every investment and trading move involves risk, and readers should conduct their own research when making a decision. "
    translated_text = translate_with_gpt(text, "BTCが不安定な週末に3％下落したため、次にこれらのビットコインの価格水準に注目する。")
    print(f"Final translated text: {translated_text}")
