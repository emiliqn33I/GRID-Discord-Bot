from dotenv import dotenv_values

config = dotenv_values(".env")

API_KEY = config["API_KEY"]
TOKEN = config["DISCORD_CLIENT_TOKEN"]
