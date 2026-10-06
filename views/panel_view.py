"""Panel principal: los botones se generan a partir de utils/ticket_types.py"""
import discord

from services.tickets import create_ticket
from utils.ticket_types import TICKET_TYPES, TicketType


class TicketButton(discord.ui.Button):
    def __init__(self, ticket_type: TicketType, row: int):
        super().__init__(
            label=ticket_type.label,
            emoji=ticket_type.emoji,
            style=discord.ButtonStyle.primary,
            custom_id=f"ticket:create:{ticket_type.key}",
            row=row,
        )
        self.ticket_type = ticket_type

    async def callback(self, interaction: discord.Interaction):
        await create_ticket(interaction, self.ticket_type)


class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for i, ticket_type in enumerate(TICKET_TYPES):
            self.add_item(TicketButton(ticket_type, row=i // 5))  # 5 botones por fila
