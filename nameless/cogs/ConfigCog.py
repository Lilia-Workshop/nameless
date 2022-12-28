import datetime
import logging
from typing import Union

import discord
from discord import app_commands
from discord.ext import commands

import nameless
from nameless.cogs.checks import BaseCheck
from nameless.shared_vars import crud_database
from NamelessConfig import NamelessConfig


__all__ = ["ConfigCog"]


class ConfigCog(commands.Cog):
    def __init__(self, bot: nameless.Nameless):
        self.bot = bot

    @commands.hybrid_group(fallback="get")
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.guilds(*getattr(NamelessConfig, "GUILD_IDs", []))
    async def config(self, ctx: commands.Context):
        """View configured properties"""
        await ctx.defer()
        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)

        assert db_guild is not None

        wc_chn = ctx.guild.get_channel(db_guild.welcome_channel_id)  # pyright: ignore
        gb_chn = ctx.guild.get_channel(db_guild.goodbye_channel_id)  # pyright: ignore

        embed: discord.Embed = (
            discord.Embed(
                title="Configured properties",
                color=discord.Color.purple(),
                timestamp=datetime.datetime.now(),
            )
            .add_field(
                name="Welcome message",
                value=db_guild.welcome_message if db_guild.welcome_message else "Unset",
            )
            .add_field(
                name="Welcome message delivery channel",
                value=wc_chn.mention if wc_chn else "Unset",
            )
            .add_field(name="Welcome message delivery allowance", value=db_guild.is_welcome_enabled)
            .add_field(
                name="Goodbye message",
                value=db_guild.goodbye_message if db_guild.goodbye_message else "Unset",
            )
            .add_field(
                name="Goodbye message delivery channel",
                value=gb_chn.mention if gb_chn else "Unset",
            )
            .add_field(name="Goodbye message delivery allowance", value=db_guild.is_goodbye_enabled)
        )
        await ctx.send(embeds=[embed])

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(message="New welcome message, max. 500 characters")
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def set_welcome_message(
        self,
        ctx: commands.Context,
        message: str,
    ):
        """Change welcome message"""
        await ctx.defer()

        if len(message) > 500:
            await ctx.send("You can not use more than 500 characters for it!")
            return

        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        assert db_guild is not None

        db_guild.welcome_message = message
        crud_database.save_changes()
        await ctx.send("Done updating welcome message")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(message="New goodbye message, max. 500 characters")
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def set_goodbye_message(
        self,
        ctx: commands.Context,
        message: str,
    ):
        """Change goodbye message"""
        await ctx.defer()

        if len(message) > 500:
            await ctx.send("You can not use more than 500 characters for it!")
            return

        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        db_guild.goodbye_message = message
        crud_database.save_changes()
        await ctx.send("Done updating goodbye message")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(dest_channel="Goodbye message delivery channel")
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def set_goodbye_channel(
        self,
        ctx: commands.Context,
        dest_channel: Union[discord.TextChannel, discord.Thread],
    ):
        """Change goodbye message delivery channel"""
        await ctx.defer()
        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        db_guild.goodbye_channel_id = dest_channel.id
        crud_database.save_changes()
        await ctx.send(f"Done updating goodbye channel to {dest_channel.mention}")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(dest_channel="Welcome message delivery channel")
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def set_welcome_channel(
        self,
        ctx: commands.Context,
        dest_channel: Union[discord.TextChannel, discord.Thread],
    ):
        """Change welcome message delivery channel"""
        await ctx.defer()
        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        db_guild.welcome_channel_id = dest_channel.id
        crud_database.save_changes()
        await ctx.send(f"Done updating welcome channel to {dest_channel.mention}")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def toggle_welcome(self, ctx: commands.Context):
        """Toggle welcome message delivery allowance"""
        await ctx.defer()
        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        db_guild.is_welcome_enabled = not db_guild.is_welcome_enabled
        crud_database.save_changes()
        await ctx.send(f"Welcome message delivery: {'on' if db_guild.is_welcome_enabled else 'off'}")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.check(BaseCheck.require_intents([discord.Intents.members]))
    async def toggle_goodbye(self, ctx: commands.Context):
        """Toggle goodbye message delivery allowance"""
        await ctx.defer()
        db_guild, _ = crud_database.get_or_create_guild_record(ctx.guild)
        db_guild.is_goodbye_enabled = not db_guild.is_goodbye_enabled
        crud_database.save_changes()
        await ctx.send(f"Goodbye message delivery: {'on' if db_guild.is_goodbye_enabled else 'off'}")

    @config.command()
    @commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def view_placeholders(self, ctx: commands.Context):
        """View available placeholders"""
        await ctx.defer()
        placeholders = {
            "{guild}": "The name of the guild.\nAvailability: Welcome+Goodbye.",
            "{@user}": "Mention that user.\nAvailability: Welcome.",
            "{name}": "Display name of that member.\nAvailability: Welcome+Goodbye.",
            "{tag}": "The 4-digit after #.\nAvailability: Welcome+Goodbye.",
        }

        await ctx.send("\n".join(f"**{key}**\n{value}\n" for key, value in placeholders.items()))


async def setup(bot: nameless.Nameless):
    await bot.add_cog(ConfigCog(bot))
    logging.info("Cog of %s added!", __name__)


async def teardown(bot: nameless.Nameless):
    await bot.remove_cog("ConfigCog")
    logging.warning("Cog of %s removed!", __name__)
