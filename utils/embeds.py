"""Todos los embeds y textos del bot. Para cambiar un mensaje, edítalo aquí."""
import discord

import config
from utils.ticket_types import TICKET_TYPES, TicketType

# Normas que aparecen en el panel
RULES = [
    "Usa los tickets solo cuando sea realmente necesario.",
    "No menciones a nadie del staff al abrirlo, y menos a Dirección o Mandos.",
    "Adjunta toda la información posible: capturas, clips y pruebas.",
    "Mantén un trato respetuoso y responde cuando el equipo te escriba.",
    "Respeta los horarios de atención, el staff también son personas.",
    f"Si pasan {config.AUTO_CLOSE_HOURS} horas sin respuesta, el ticket se cerrará automáticamente.",
    "Incumplir estas normas puede conllevar sanciones.",
]


def panel_embed() -> discord.Embed:
    rules = "\n".join(f"🔹 {r}" for r in RULES)
    types = "\n".join(
        f"{t.emoji} **{t.label}:** {t.description}" for t in TICKET_TYPES
    )
    description = (
        "✈️ **Antes de abrir un ticket, lee esto:**\n\n"
        f"{rules}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "**Elige la categoría que mejor encaje con tu caso:**\n\n"
        f"{types}"
    )
    embed = discord.Embed(
        title="🎫 Centro de Atención · Barajas PD",
        description=description,
        color=config.EMBED_COLOR,
    )
    if config.BANNER_URL:
        embed.set_image(url=config.BANNER_URL)
    embed.set_footer(text=config.FOOTER_TEXT)
    return embed


def ticket_welcome_embed(ticket_type: TicketType, user: discord.abc.User) -> discord.Embed:
    embed = discord.Embed(
        title=f"{ticket_type.emoji} Ticket · {ticket_type.label}",
        description=(
            f"Hola {user.mention}, gracias por contactar con el equipo de **Barajas PD**.\n\n"
            "Explica tu caso con el mayor detalle posible y adjunta las pruebas necesarias.\n"
            "Un miembro del staff te atenderá en cuanto pueda."
        ),
        color=config.EMBED_COLOR,
    )
    embed.add_field(name="Categoría", value=f"{ticket_type.emoji} {ticket_type.label}", inline=True)
    embed.add_field(name="Usuario", value=user.mention, inline=True)
    embed.set_footer(text=config.FOOTER_TEXT)
    return embed


def ticket_log_embed(channel_name: str, ticket_type_label: str, owner_id: int,
                     closed_by: str, reason: str) -> discord.Embed:
    embed = discord.Embed(title="📁 Ticket cerrado", color=0xE11D48)
    embed.add_field(name="Canal", value=f"#{channel_name}", inline=True)
    embed.add_field(name="Categoría", value=ticket_type_label, inline=True)
    embed.add_field(name="Creador", value=f"<@{owner_id}>", inline=True)
    embed.add_field(name="Cerrado por", value=closed_by, inline=True)
    embed.add_field(name="Motivo", value=reason, inline=False)
    embed.set_footer(text=config.FOOTER_TEXT)
    return embed
