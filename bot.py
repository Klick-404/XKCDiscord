#!/usr/bin/env python3
import asyncio
import discord
import os
import requests
from dotenv import load_dotenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)
xkcd_url = 'http://xkcd.com/info.0.json'
latest_comic_number = None

load_dotenv()
channel_id = int(os.getenv("XKCD_CHANNEL_ID"))
bot_token = os.getenv("XKCD_TOKEN")

async def check_xkcd():
    global latest_comic_number
    response = requests.get(xkcd_url)
    if response.status_code == 200:
        data = response.json()
        if latest_comic_number is None:
            latest_comic_number = data['num']
        elif latest_comic_number < data['num']:
            latest_comic_number = data['num']
            comic_url = f'https://xkcd.com/{data["num"]}/'
            comic_image_url = data['img']
            channel = client.get_channel(channel_id)
            await channel.send(f'XKCD just uploaded a new comic! {comic_url}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    while True:
        await check_xkcd()
        await asyncio.sleep(60606) # Check for new XKCD comic every 6 hours

client.run(bot_token)
