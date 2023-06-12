# -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv
from briefings import briefings
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def request_translation(func, text, translated_title=None, target_language="japanese", num_retries=3, retry_delay=150):
    for i in range(num_retries):
        try:
            if func.__name__ == "translate_text":
                response = func(text, translated_title, target_language)
            else:
                response = func(text, target_language)
            if response is not None:
                return response
        except Exception as e:
            if i < num_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                raise e
    return None

def translate_text(text, translated_title, target_language="japanese"):
    print('translating...')
    briefing = [b for b in briefings if b['language'] == target_language][0]
    briefing = briefing['main'] + briefing['article']
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": briefing},
                {"role": "user", "content": text},
            ],
            max_tokens=5000,
            temperature=0.8,
            top_p=0.7,
            # request_timeout=900,
            n=1,
        )

        translated_text = response.choices[0].message.content.strip()
        # print("chunk: "+translated_text)ß
        return translated_text

    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return None

def translate_title(text, target_language="japanese"):
    briefing = [b for b in briefings if b['language'] == target_language][0]
    briefing = briefing['main'] + briefing['headline']
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
    translated_text = translate_text(text, "BTCが不安定な週末に3％下落したため、次にこれらのビットコインの価格水準に注目する。")
    print(f"Final translated text: {translated_text}")
