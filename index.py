# bot.py
import discord
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

def send_message(message):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        client.loop.create_task(channel.send(message))

client.run(DISCORD_TOKEN)
