"""Botones dentro de cada ticket: Reclamar y Cerrar."""
import discord

import config
from services.tickets import close_ticket
from utils import storage
from utils.permissions import is_staff


class ConfirmCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)

    @discord.ui.button(label="Sí, cerrar", emoji="✅", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="🔒 Cerrando ticket...", view=None)
        await close_ticket(interaction.channel, interaction.user, "Cerrado desde el botón")

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Cancelado.", view=None)


class TicketControlsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reclamar", emoji="🙋", style=discord.ButtonStyle.success,
                       custom_id="ticket:claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not is_staff(interaction.user):
            await interaction.response.send_message("❌ Solo el staff puede reclamar tickets.",
                                                    ephemeral=True)
            return
        storage.update_ticket(interaction.channel.id, claimed_by=interaction.user.id)
        embed = discord.Embed(
            description=f"🙋 {interaction.user.mention} ha reclamado este ticket.",
            color=config.EMBED_COLOR,
        )
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Cerrar", emoji="🔒", style=discord.ButtonStyle.danger,
                       custom_id="ticket:close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = storage.get_ticket(interaction.channel.id)
        if ticket is None:
            await interaction.response.send_message("❌ Este canal no es un ticket.", ephemeral=True)
            return
        if not (is_staff(interaction.user) or interaction.user.id == ticket["user_id"]):
            await interaction.response.send_message("❌ No puedes cerrar este ticket.", ephemeral=True)
            return
        await interaction.response.send_message("¿Seguro que quieres cerrar el ticket?",
                                                view=ConfirmCloseView(), ephemeral=True)
