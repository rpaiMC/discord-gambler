import discord
import json
import os
import time

def setup_economy(tree, bank):
    COOLDOWN_FILE = "data/cooldowns.json"
    DAILY_AMOUNT = 10000
    SECONDS_PER_DAY = 86400

    def load_cooldowns():
        if not os.path.exists(COOLDOWN_FILE):
            return {}
        with open(COOLDOWN_FILE, "r") as f:
            return json.load(f)

    def save_cooldowns(data):
        with open(COOLDOWN_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @tree.command(name="daily", description="Claim your daily $10,000")
    async def daily(interaction: discord.Interaction):
        cooldowns = load_cooldowns()
        user_id = str(interaction.user.id)
        now = int(time.time())

        last_claimed = cooldowns.get(user_id, 0)
        if now - last_claimed < SECONDS_PER_DAY:
            remaining = SECONDS_PER_DAY - (now - last_claimed)
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await interaction.response.send_message(
                f"You already claimed your daily reward. Try again in {hours}h {minutes}m.",
                ephemeral=True
            )
            return

        bank.update_balance(interaction.user.id, DAILY_AMOUNT)
        cooldowns[user_id] = now
        save_cooldowns(cooldowns)

        await interaction.response.send_message(
            f"✅ You claimed your daily reward of ${DAILY_AMOUNT}!"
        )

    @tree.command(name="bank", description="Check your current bank balance")
    async def bank_cmd(interaction: discord.Interaction):
        bal = bank.get_balance(interaction.user.id)
        embed = discord.Embed(
            title="🏦 Your Bank Balance",
            description=f"You currently have ${bal}.",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
