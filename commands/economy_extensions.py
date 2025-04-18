
import discord
from discord import app_commands
import random

def setup_economy_extensions(tree, bank):
    # Admin-only group
    economy_group = app_commands.Group(name="economy", description="Admin money commands")

    @economy_group.command(name="money", description="Add or remove money (admin only)")
    @app_commands.describe(user="User to modify", amount="Amount to add or remove (use negative to subtract)")
    async def money(interaction: discord.Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("🚫 You must be an admin to use this command.", ephemeral=True)
            return

        bank.update_balance(user.id, amount)
        updated = bank.get_balance(user.id)

        embed = discord.Embed(
            title="💰 Money Updated",
            description=f"<@{user.id}>'s new balance: `${updated}`",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

    @tree.command(name="slots", description="Spin the slot machine and try your luck")
    @app_commands.describe(bet="How much you want to bet")
    async def slots(interaction: discord.Interaction, bet: int):
        balance = bank.get_balance(interaction.user.id)
        if bet > balance or bet <= 0:
            await interaction.response.send_message(f"Invalid bet. Your balance is ${balance}.", ephemeral=True)
            return

        symbols = ["🍒", "🍋", "🔔", "⭐", "🍇", "💎"]
        spin = [random.choice(symbols) for _ in range(3)]

        embed = discord.Embed(
            title="🎰 Slot Machine",
            description=f"`| {' | '.join(spin)} |`",
            color=discord.Color.purple()
        )

        # Evaluate result
        if spin[0] == spin[1] == spin[2]:
            winnings = bet * 10
            bank.update_balance(interaction.user.id, winnings)
            result = f"💥 JACKPOT! You won ${winnings}!"
        elif spin.count(spin[0]) == 2 or spin.count(spin[1]) == 2:
            winnings = int(bet * 1.5)
            bank.update_balance(interaction.user.id, winnings)
            result = f"✨ Nice! You won ${winnings}!"
        else:
            bank.update_balance(interaction.user.id, -bet)
            result = f"😢 You lost ${bet}."

        embed.add_field(name="Result", value=result, inline=False)
        await interaction.response.send_message(embed=embed)

    tree.add_command(economy_group)
