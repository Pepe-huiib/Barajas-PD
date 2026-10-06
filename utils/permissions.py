import discord

import config


def is_staff(member: discord.Member) -> bool:
    if member.guild_permissions.administrator:
        return True
    return any(role.id in config.STAFF_ROLE_IDS for role in member.roles)
