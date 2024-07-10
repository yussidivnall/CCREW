# bot.py
import os

import discord
import config

TOKEN = config.discord_token

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel_id = config.discord_channel_id
    img = "images/snapshot.png"

    print(f"{client.user} has connected to Discord!")
    channel = client.get_channel(channel_id)
    if not channel:
        print(f"No such channel {channel_id}")
        return
    await channel.send(content="Content", file=discord.File(img))
    await client.close()


client.run(TOKEN)
