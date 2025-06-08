""" import asyncio
import aiohttp
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
from RAUSHAN import *
from pyrogram import *
from fuzzywuzzy import fuzz

plt.style.use('dark_background')

crypto_names = [
    "bitcoin", "ethereum", "tether", "bnb", "usdcoin", "xrp", 
    "cardano", "dogecoin", "solana", "polygon", 
    "polkadot", "litecoin", "avalanche", "shibainu", "tron", 
    "dai", "cosmos", "chainlink", "uniswap", "algorand",
    "filecoin", "monero", "nearprotocol", "ethereumclassic", "vechain", 
    "tezos", "fantom", "bitcoincash", "decentraland", "hedera", 
    "elrond", "thetanetwork", "internetcomputer", "eos", "thesandbox",
    "aave", "quant", "flow", "klaytn", "helium",
    "terra", "thorchain", "maker", "bittorrentnew", "stacks",
    "harmony", "neo", "curvedaotoken", "waves", "nexo",
    "pancakeswap", "loopring", "kadena", "mina", "zcash",
    "enjincoin", "chiliz", "basicattentiontoken", "sushiswap", "holo",
    "kusama", "celsius", "arweave", "decred", "bitcoinsv",
    "compound", "synthetix", "0x", "horizen", "qtum",
    "siacoin", "ravencoin", "icon", "zilliqa", "dash",
    "nem", "iost", "omgnetwork", "energywebtoken", "bancor",
    "digibyte", "augur", "fetchai", "livepeer", "storj",
    "gnosis", "lisk", "oceanprotocol", "status", "civic"
]

async def fetch_crypto_details(session, crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}"
    async with session.get(url) as response:
        if response.status != 200 or 'error' in await response.json():
            return "N/A", "N/A", "N/A", "N/A", "N/A"

        data = await response.json()
        current_price_usd = data['market_data']['current_price']['usd']
        high_price_usd = data['market_data']['high_24h']['usd']
        low_price_usd = data['market_data']['low_24h']['usd']
        percent_change = data['market_data']['price_change_percentage_24h']
        launch_date = data['genesis_date'] if 'genesis_date' in data else "N/A"

        return current_price_usd, high_price_usd, low_price_usd, percent_change, launch_date

async def fetch_historical_prices(session, crypto):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=7"
    async with session.get(url) as response:
        if response.status != 200 or 'error' in await response.json():
            return [], []

        data = await response.json()
        prices = [item[1] for item in data['prices']]
        timestamps = [datetime.fromtimestamp(item[0] / 1000) for item in data['prices']]
        
        return timestamps, prices

def plot_crypto_price(timestamps, prices, crypto):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, prices, label=f'{crypto.capitalize()} Price (USD)', color='cyan')
    plt.title(f'{crypto.capitalize()} Price Over the Last Week')
    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.xticks(rotation=45)
    plt.legend()
    image_path = f'{crypto}_performance.png'
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()
    
    return image_path

def format_caption(crypto, current_price, high_price, low_price, percent_change, launch_date):
    caption = (f"**{crypto.capitalize()} Performance**\n\n"
               f"**Current Price (USD):** $`{current_price}`\n"
               f"**High Price (24h):** $`{high_price}`\n"
               f"**Low Price (24h):** $`{low_price}`\n"
               f"**Launch Date:** `{launch_date}`\n"
               f"**Percentage Change (24h):** `{percent_change}%`\n")
    
    return caption

def search_crypto(search_term, threshold=80):
    normalized_search_term = search_term.lower().replace(" ", "")

    best_match = None
    best_ratio = 0

    for crypto_name in crypto_names:
        ratio = fuzz.ratio(normalized_search_term, crypto_name)
        if ratio > best_ratio and ratio >= threshold:
            best_match = crypto_name
            best_ratio = ratio

    return best_match

@RAUSHAN.on_message(filters.command("crypto", prefixes=HANDLER) & filters.user('me'))
async def crypto_graph(_, message):
    if len(message.command) < 2:
        return await message.edit("Please enter a crypto name!")

    crypto = message.text.split(None, 1)[1].lower()
    if crypto not in crypto_names:
        crypto = search_crypto(crypto)
        
    async with aiohttp.ClientSession() as session:
        current_price, high_price, low_price, percent_change, launch_date = await fetch_crypto_details(session, crypto)

        if current_price == "N/A":
            return await message.edit("Could not fetch current price. Please check the cryptocurrency name.")

        timestamps, prices = await fetch_historical_prices(session, crypto)

        if not timestamps:
            return await message.edit("Could not fetch historical prices. Please check the cryptocurrency name.")

        image_path = plot_crypto_price(timestamps, prices, crypto)
        caption = format_caption(crypto, current_price, high_price, low_price, percent_change, launch_date)
        await message.reply_photo(photo=image_path, caption=caption)
