
import discord
from discord.ext import commands
from bank import Bank
from games.coinflip import setup_coinflip
from games.blackjack import setup_blackjack

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
bank = Bank("data/bank.json")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

setup_coinflip(tree, bank)
setup_blackjack(tree, bank)

bot.run("YOUR_DISCORD_BOT_TOKEN")
