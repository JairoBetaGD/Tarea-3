import json

class MemesHandler:

    def __init__(self, filename):
        self.filename = filename
        self.memes = self.load_memes()

    def load_memes(self):
        with open(self.filename, 'r') as file:
            memes_data = json.load(file)
        return memes_data["memes_links"]

    def add_meme(self, url):
        memes = self.memes
        id = int(memes[-1]["ID"]) + 1
        new_meme = {"ID": str(id), "meme": url}
        memes.append(new_meme)
        with open(self.filename, 'w') as file:
            json.dump({"memes_links": memes}, file)
        return new_meme