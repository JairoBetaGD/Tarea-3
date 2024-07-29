from commands.command_base import Command, send_message
import discord
import asyncio

class TempOpenCommand(Command):
    async def execute(self):
        required_role_name = "Ω★★★ ADMINISTRACIÓN ★★★Ω"  # Reemplaza con el nombre del rol requerido

        # Verificar si el autor tiene el rol requerido
        has_required_role = any(role.name == required_role_name for role in self.message.author.roles)
        if not has_required_role:
            await send_message(self.message.channel, "No tienes el rol necesario para usar este comando.")
            return

        # Verificar si se proporcionaron los argumentos necesarios
        args = self.message.content.split()
        if len(args) != 3:
            await send_message(self.message.channel, "Uso incorrecto del comando. Ejemplo: `!temp_open #canal minutos`")
            return

        # Obtener el canal mencionado
        channel_arg = args[1]
        if not channel_arg.startswith("<#") or not channel_arg.endswith(">"):
            await send_message(self.message.channel, "Debes mencionar un canal válido usando #.")
            return
        channel_id = int(channel_arg[2:-1])
        channel = self.message.guild.get_channel(channel_id)
        if not channel:
            await send_message(self.message.channel, "No se encontró el canal especificado.")
            return

        # Obtener el tiempo en minutos
        try:
            minutes = int(args[2])
        except ValueError:
            await send_message(self.message.channel, "Por favor, proporciona un valor numérico válido para los minutos.")
            return

        # Permitir el envío de mensajes en el canal
        await channel.set_permissions(self.message.guild.default_role, send_messages=True)

        await send_message(self.message.channel, f"Canal {channel.mention} abierto por {minutes} minutos.")

        # Esperar y luego restablecer los permisos del canal
        await asyncio.sleep(minutes * 60)
        await channel.set_permissions(self.message.guild.default_role, send_messages=False)
        await send_message(self.message.channel, f"Canal {channel.mention} cerrado después de {minutes} minutos.")
