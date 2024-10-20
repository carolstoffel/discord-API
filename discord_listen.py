import os

import discord
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the Discord token from environment variables
discord_token = os.getenv("DISCORD_TOKEN")
cat_fact_url = os.getenv("CAT_FACT_URL")
conversion_currency_url = os.getenv("CONVERSION_CURR_URL")
# Create a Discord client instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info('Logged on as %s', client.user)

@client.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == client.user:
        return

    if message.content.startswith('$cat'):
        response = requests.get(cat_fact_url)
        assert response.status_code == 200
        assert "fact" in response.json()
        
        logging.info(f"Sending cat fact {response.json()['fact']}")

        await message.channel.send(response.json()['fact'])

    if message.content.startswith('$usd'):
        response = requests.get(f"{conversion_currency_url}usd.json")
        
        logging.info(f"Sending conversion from USD to CLP {response.json()['usd']['clp']}")

        await message.channel.send(f"1 USD = {response.json()['usd']['clp']} CLP")
        
client.run(discord_token)

