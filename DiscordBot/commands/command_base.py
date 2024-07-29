import discord

class Command:
    def __init__(self, message):
        self.message = message

    async def execute(self):
        raise NotImplementedError

async def send_message(channel, content):
    await channel.send(content)


