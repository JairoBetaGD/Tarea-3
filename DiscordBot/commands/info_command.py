from commands.command_base import Command, send_message


class InfoCommand(Command):
    async def execute(self):
        await send_message(self.message.channel,"Hola! soy un bot creado por JairoBetaGD, en que les ayudo?")