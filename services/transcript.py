import discord


async def build_transcript(channel: discord.TextChannel) -> str:
    lines = [f"Transcripción de #{channel.name}", "=" * 40]
    async for m in channel.history(limit=None, oldest_first=True):
        ts = m.created_at.strftime("%d/%m/%Y %H:%M")
        content = m.clean_content or ("[embed]" if m.embeds else "")
        for a in m.attachments:
            content += f"\n    [adjunto] {a.url}"
        lines.append(f"[{ts}] {m.author}: {content}")
    return "\n".join(lines)
