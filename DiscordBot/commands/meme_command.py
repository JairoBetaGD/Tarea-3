from commands.command_base import Command, send_message
import random
import json

class MemeCommand(Command):
    async def execute(self):
        with open('Meme.json') as file:
            data = json.load(file)
        random_index = random.randint(0, len(data['memes_links']) - 1)
        selected_meme = data['memes_links'][random_index]['meme']
        await send_message(self.message.channel, selected_meme)