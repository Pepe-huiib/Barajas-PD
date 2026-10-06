"""Comandos slash y tareas automáticas del sistema de tickets."""
import time

import discord
from discord import app_commands
from discord.ext import commands, tasks

import config
from services.tickets import close_ticket
from utils import storage
from utils.embeds import panel_embed
from utils.permissions import is_staff
from views.panel_view import PanelView


class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_close.change_interval(minutes=config.AUTO_CLOSE_CHECK_MINUTES)
        self.auto_close.start()

    async def cog_unload(self):
        self.auto_close.cancel()

    # ---------- Comandos ----------
    @app_commands.command(name="panel", description="Envía el panel de tickets a este canal")
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def panel(self, interaction: discord.Interaction):
        await interaction.channel.send(embed=panel_embed(), view=PanelView())
        await interaction.response.send_message("✅ Panel enviado.", ephemeral=True)

    @app_commands.command(name="cerrar", description="Cierra el ticket actual")
    @app_commands.describe(motivo="Motivo del cierre")
    @app_commands.guild_only()
    async def cerrar(self, interaction: discord.Interaction,
                     motivo: str = "Sin motivo especificado"):
        ticket = storage.get_ticket(interaction.channel_id)
        if ticket is None:
            await interaction.response.send_message("❌ Esto no es un ticket.", ephemeral=True)
            return
        if not (is_staff(interaction.user) or interaction.user.id == ticket["user_id"]):
            await interaction.response.send_message("❌ No puedes cerrar este ticket.", ephemeral=True)
            return
        await interaction.response.send_message("🔒 Cerrando...", ephemeral=True)
        await close_ticket(interaction.channel, interaction.user, motivo)

    @app_commands.command(name="agregar", description="Añade a un usuario al ticket")
    @app_commands.guild_only()
    async def agregar(self, interaction: discord.Interaction, usuario: discord.Member):
        if storage.get_ticket(interaction.channel_id) is None:
            await interaction.response.send_message("❌ Esto no es un ticket.", ephemeral=True)
            return
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Solo el staff.", ephemeral=True)
            return
        await interaction.channel.set_permissions(
            usuario, view_channel=True, send_messages=True,
            attach_files=True, read_message_history=True)
        await interaction.response.send_message(f"✅ {usuario.mention} añadido al ticket.")

    @app_commands.command(name="quitar", description="Quita a un usuario del ticket")
    @app_commands.guild_only()
    async def quitar(self, interaction: discord.Interaction, usuario: discord.Member):
        if storage.get_ticket(interaction.channel_id) is None:
            await interaction.response.send_message("❌ Esto no es un ticket.", ephemeral=True)
            return
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Solo el staff.", ephemeral=True)
            return
        await interaction.channel.set_permissions(usuario, overwrite=None)
        await interaction.response.send_message(f"✅ {usuario.mention} quitado del ticket.")

    # ---------- Actividad (para el cierre automático) ----------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return
        if storage.get_ticket(message.channel.id):
            storage.update_ticket(message.channel.id, last_activity=time.time())

    # ---------- Cierre automático por inactividad ----------
    @tasks.loop(minutes=10)
    async def auto_close(self):
        limit = config.AUTO_CLOSE_HOURS * 3600
        now = time.time()
        for channel_id, data in list(storage.all_tickets().items()):
            if now - data["last_activity"] < limit:
                continue
            channel = self.bot.get_channel(int(channel_id))
            if channel is None:  # El canal ya no existe
                storage.remove_ticket(int(channel_id))
                continue
            await close_ticket(channel, None,
                               f"Inactividad ({config.AUTO_CLOSE_HOURS}h sin respuesta)")

    @auto_close.before_loop
    async def before_auto_close(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
