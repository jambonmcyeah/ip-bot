import discord
import logic

class Bot(discord.Client):
    def __init__(self, config: dict, *args, loop=None, **options):
        super().__init__(*args, loop=loop, **options)
        self.ip_getter = logic.IpGetter()
        self.config = config
        self.COMMANDS = {
            "eip": self.ip_getter.get_external_ip,
            "pip": self.ip_getter.get_local_ip
        }

    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.DMChannel) and message.author.id in self.config['whitelist']:
            if message.content.startswith("!"):
                try:
                    reply = await self.COMMANDS[message.content[1:]]()
                    await message.channel.send(reply)
                except TimeoutError as e:
                    await message.channel.send("Internal Error: " + str(e.args))
                except KeyError:
                    await message.channel.send("Error: Command Not Found")
            

