import json

import bot

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    client = bot.Bot(config)
    client.run(config["token"])