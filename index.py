import discord
import os
import dotenv
import asyncio
from aiohttp import web

dotenv.load_dotenv()  # Load environment variables from .env file

intents = discord.Intents.default()
client = discord.Client(intents=intents)  # Initialize Discord client with default intents

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Get Discord token from environment variables
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Get channel ID from environment variables
THREAD_ID = os.getenv('THREAD_ID')  # Get thread ID from environment variables (optional)

# Asynchronous function to send a message to the specified Discord thread
async def send_message(message):
    await client.wait_until_ready()  # Wait until the client is fully ready
    channel = client.get_channel(CHANNEL_ID)  # Get the channel by ID
    if channel:
        print(f"Channel found: {channel.name}")  # Debugging line
        thread = None
        if THREAD_ID:
            thread = channel.get_thread(int(THREAD_ID))  # Get the thread by ID
            print(f"Using existing thread: {thread}")  # Debugging line
        if not thread:
            # Create a new thread if it doesn't exist
            thread = await channel.create_thread(name="GitHub Updates", auto_archive_duration=60)
            print(f"Created new thread: {thread.name}")  # Debugging line
        await thread.send(message)  # Send the message to the thread
        print(f"Message sent: {message}")  # Debugging line
    else:
        print(f"Channel not found: {CHANNEL_ID}")  # Debugging line

# AIOHTTP request handler to handle incoming messages
async def handle(request):
    data = await request.json()  # Parse JSON payload
    message = data.get('message')
    if message:
        await send_message(message)  # Send the message to the Discord thread
    return web.Response(text="Message sent")  # Respond with a confirmation

# Initialize the AIOHTTP web application
async def init_app():
    app = web.Application()
    app.router.add_post('/send-message', handle)  # Set up the route to handle POST requests
    return app

# Event handler for when the Discord bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')  # Debugging line
    app = await init_app()  # Initialize the web application
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)  # Run the web application on localhost port 8080
    await site.start()

client.run(DISCORD_TOKEN)  # Run the Discord bot with the provided token
