# index.py
import discord
import os
import dotenv
import asyncio
from aiohttp import web

dotenv.load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
THREAD_ID = os.getenv('THREAD_ID')

async def send_message(message):
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        print(f"Channel found: {channel.name}")  # Debugging line
        thread = None
        if THREAD_ID:
            thread = channel.get_thread(int(THREAD_ID))
            print(f"Using existing thread: {thread}")  # Debugging line
        if not thread:
            thread = await channel.create_thread(name="GitHub Updates", auto_archive_duration=60)
            print(f"Created new thread: {thread.name}")  # Debugging line
        await thread.send(message)
        print(f"Message sent: {message}")  # Debugging line
    else:
        print(f"Channel not found: {CHANNEL_ID}")  # Debugging line

async def handle(request):
    data = await request.json()
    message = data.get('message')
    if message:
        await send_message(message)
    return web.Response(text="Message sent")

async def init_app():
    app = web.Application()
    app.router.add_post('/send-message', handle)
    return app

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

client.run(DISCORD_TOKEN)
