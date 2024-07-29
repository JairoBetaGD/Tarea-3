from commands.command_base import Command, send_message
import time, json
from JsonMemes import MemesHandler

class AddMemeCommand(Command):
    async def execute(self):
        words = self.message.content.split()
        if len(words) == 2:
            url = words[1]

            filename = "Meme.json"
            memes = self.load_memes(filename)

            id = int(memes[-1]["ID"]) + 1
            new_meme = {"ID": str(id), "meme": url}
            memes.append(new_meme)

            self.save_memes(filename, memes)

            await send_message(self.message.channel,
                               f"Se ha agregado un nuevo meme con ID {new_meme['ID']}.")
            time.sleep(3)
            await send_message(self.message.channel,
                               "Tendrás que esperar hasta que me vuelva a activar, así podrás ver el meme que agregaste")
        else:
            await send_message(self.message.channel,
                               "Por favor, proporciona solo una URL después del comando.")

    def load_memes(self, filename):
        with open(filename, 'r') as file:
            memes_data = json.load(file)
        return memes_data["memes_links"]

    def save_memes(self, filename, memes):
        with open(filename, 'w') as file:
            json.dump({"memes_links": memes}, file)