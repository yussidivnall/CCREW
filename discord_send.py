import logging
from discord_webhook import DiscordWebhook
import config
import argparse


def dispatch_message(message, image=None):
    # Post a message to discord
    logging.info(f"discord msg: {message}")
    webhook = DiscordWebhook(url=config.discord_webhook_url, content=message)
    if image:
        with open(image, "rb") as f:
            webhook.add_file(f.read(), filename="monitoring.png")
    webhook.execute()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("msg")
    args = parser.parse_args()
    dispatch_message(args.msg)
