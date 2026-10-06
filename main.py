"""Punto de entrada. Ejecutar con:  python main.py"""
import discord
from discord.ext import commands

import config
from views.panel_view import PanelView
from views.ticket_controls import TicketControlsView


class BarajasBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Necesario para las transcripciones
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Cargar módulos
        for ext in config.COGS:
            await self.load_extension(ext)

        # Vistas persistentes: los botones siguen funcionando tras reiniciar el bot
        self.add_view(PanelView())
        self.add_view(TicketControlsView())

        # Sincronizar comandos slash en tu servidor (aparecen al instante)
        guild = discord.Object(id=config.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f"✅ Conectado como {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    if not config.TOKEN:
        raise SystemExit("❌ Falta DISCORD_TOKEN en el archivo .env")
    BarajasBot().run(config.TOKEN)
