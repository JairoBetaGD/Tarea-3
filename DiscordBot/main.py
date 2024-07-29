# Importes
import discord
from commands.command_base import Command, send_message
from commands.info_command import InfoCommand
from commands.meme_command import MemeCommand
from commands.add_meme_command import AddMemeCommand
from commands.temp_open_command import TempOpenCommand
from commands.hunger_games_command import HungerGamesCommand



#token
TOKEN = input("Ingrese token:")

# Declaraciones de variables
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

Prefix = "??"

# Comandos
commands = {
    "info": InfoCommand,
    "meme": MemeCommand,
    "add_meme": AddMemeCommand,
    "temp_open": TempOpenCommand,
    "hunger_games": HungerGamesCommand,
    
    #Mas comandos
}

# Eventos
@client.event
async def on_ready():
    print("Bot Activado")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(Prefix):
        command_name = message.content[len(Prefix):].split()[0]
        if command_name in commands:
            command = commands[command_name](message)
            await command.execute()

client.run(TOKEN) 
