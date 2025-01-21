import logging
import os
import sys

import discord
from discord.ext.commands import when_mentioned_or
from dotenv import load_dotenv

from nameless import Nameless

load_dotenv()

is_debug: bool = bool(int(os.getenv("DEBUG", 0)))

discord.utils.setup_logging(level=logging.DEBUG if is_debug else logging.INFO)
logging.getLogger().name = "nameless"

nameless = Nameless(prefix=when_mentioned_or("nl."))

nameless.start_bot(is_debug=is_debug)
