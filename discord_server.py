import logging
from flask import Flask

app = Flask(__name__)
import discord
from . import config


TOKEN = config.discord_token

intents = discord.Intents.default()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logging.error("Client ready")
    channel_id = config.discord_channel_id
    img = "images/snapshot.png"

    print(f"{client.user} has connected to Discord!")
    channel = client.get_channel(channel_id)
    if not channel:
        logging.error(f"No such channel {channel_id}")
        return
    else:
        logging.error(f"channel %{channel}")
    channel.send("Ready")


@app.route("/post")
async def post():
    # await channel.send(content="Content", file=discord.File(img))
    channel_id = config.discord_channel_id
    channel = client.get_channel(channel_id)
    if not channel:
        logging.error("No Channel")
        return "No Channel"
    channel.send("Hi")
    channel.send(content="Content")
    return ""


@app.route("/")
def home():
    logging.error("home")
    return "Hi"


if __name__ == "__main__":

    logging.error("Starting")
    client.run(TOKEN)
    while not client.is_ready():
        pass
    app.run()
