import requests
import discord
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)
channel_id = #channel ID goes here
xkcd_url = 'http://xkcd.com/info.0.json'
latest_comic_number = None

async def check_xkcd():
    global latest_comic_number
    response = requests.get(xkcd_url)
    if response.status_code == 200:
        data = response.json()
        if latest_comic_number is None:
            latest_comic_number = data['num']
        elif latest_comic_number < data['num']:
            latest_comic_number = data['num']
            comic_url = f'https://xkcd.com/%7Bdata[%22num%22]%7D/'
            comic_image_url = data['img']
            channel = client.get_channel(channel_id)
            await channel.send(f'XKCD just uploaded a new comic! {comic_url}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await check_xkcd()
    while True:
        await asyncio.sleep(60606) # Check for new XKCD comic every 6 hours
        await check_xkcd()
        print("test")

client.run('bot token goes here')
