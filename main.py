
import discord
from discord.ext import commands
import os
import sys

sys.path.append(os.path.dirname(__file__))

from bank import Bank
from games.blackjack import setup_blackjack
from games.mines import setup_mines
from games.coinflip import setup_coinflip
from commands.economy import setup_economy
from commands.economy_extensions import setup_economy_extensions

DEV_GUILD_ID = None  # Set this to your server ID for instant sync, or leave None for global

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
bank = Bank("data/bank.json")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        if DEV_GUILD_ID:
            guild = discord.Object(id=DEV_GUILD_ID)
            synced = await tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to dev guild.")
        else:
            synced = await tree.sync()
            print(f"Synced {len(synced)} global commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

setup_coinflip(tree, bank)
setup_blackjack(tree, bank)
setup_mines(tree, bank)
setup_economy(tree, bank)
setup_economy_extensions(tree, bank)




bot.run("YOUR_BOT_TOKEN_HERE")
