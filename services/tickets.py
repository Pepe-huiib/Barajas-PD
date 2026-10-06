"""
LÓGICA DE TICKETS: crear y cerrar.
Los botones y comandos solo llaman a estas funciones.
"""
import asyncio
import io

import discord

import config
from services.transcript import build_transcript
from utils import storage
from utils.embeds import ticket_log_embed, ticket_welcome_embed
from utils.ticket_types import TicketType, get_type


async def create_ticket(interaction: discord.Interaction, ticket_type: TicketType) -> None:
    # Import aquí para evitar importaciones circulares
    from views.ticket_controls import TicketControlsView

    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    member = interaction.user

    # Límite de tickets por usuario
    open_ids = storage.get_open_tickets_of_user(member.id)
    if len(open_ids) >= config.MAX_OPEN_TICKETS_PER_USER:
        await interaction.followup.send(
            f"❌ Ya tienes un ticket abierto: <#{open_ids[0]}>", ephemeral=True
        )
        return

    category = guild.get_channel(ticket_type.category_id or config.TICKETS_CATEGORY_ID)

    # Permisos del canal
    base = dict(view_channel=True, send_messages=True, attach_files=True,
                embed_links=True, read_message_history=True)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(**base),
        guild.me: discord.PermissionOverwrite(**base, manage_channels=True),
    }
    for role_id in (*config.STAFF_ROLE_IDS, *ticket_type.extra_role_ids):
        role = guild.get_role(role_id)
        if role:
            overwrites[role] = discord.PermissionOverwrite(**base, manage_messages=True)

    channel = await guild.create_text_channel(
        name=f"{ticket_type.key}-{member.name}"[:90],
        category=category if isinstance(category, discord.CategoryChannel) else None,
        overwrites=overwrites,
        topic=f"Ticket de {member} ({member.id}) | {ticket_type.label}",
        reason=f"Ticket abierto por {member}",
    )

    storage.add_ticket(channel.id, member.id, ticket_type.key)

    await channel.send(
        content=member.mention,
        embed=ticket_welcome_embed(ticket_type, member),
        view=TicketControlsView(),
    )
    await interaction.followup.send(f"✅ Ticket creado: {channel.mention}", ephemeral=True)


async def close_ticket(channel: discord.TextChannel,
                       closed_by: discord.abc.User | None,
                       reason: str = "Sin motivo especificado") -> None:
    data = storage.get_ticket(channel.id)
    if data is None:
        return

    closer = closed_by.mention if closed_by else "Sistema (automático)"
    ticket_type = get_type(data["type"])
    type_label = f"{ticket_type.emoji} {ticket_type.label}" if ticket_type else data["type"]

    # Enviar transcripción al canal de logs
    log_channel = channel.guild.get_channel(config.LOGS_CHANNEL_ID)
    if log_channel:
        transcript = await build_transcript(channel)
        file = discord.File(io.BytesIO(transcript.encode("utf-8")),
                            filename=f"transcript-{channel.name}.txt")
        await log_channel.send(
            embed=ticket_log_embed(channel.name, type_label, data["user_id"], closer, reason),
            file=file,
        )

    storage.remove_ticket(channel.id)

    try:
        await channel.send(f"🔒 Ticket cerrado por {closer}. Motivo: **{reason}**\n"
                           "El canal se eliminará en 5 segundos.")
        await asyncio.sleep(5)
        await channel.delete(reason=f"Ticket cerrado: {reason}")
    except discord.NotFound:
        pass
