from typing import TypeAlias

import discord

__all__ = ["NamelessTextable"]

NamelessTextable: TypeAlias = (
    discord.TextChannel | discord.Thread | discord.VoiceChannel
)
"""Channels that retrieving & sending data without quirks."""
