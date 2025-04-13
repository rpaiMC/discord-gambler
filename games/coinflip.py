
import random
import discord

def setup_coinflip(tree, bank):
    @tree.command(name="coinflip", description="Flip a coin and bet on heads or tails")
    async def coinflip(interaction: discord.Interaction, bet: int, guess: str):
        guess = guess.lower()
        if guess not in ['heads', 'tails']:
            await interaction.response.send_message("Choose either 'heads' or 'tails'.", ephemeral=True)
            return

        balance = bank.get_balance(interaction.user.id)
        if bet > balance or bet <= 0:
            await interaction.response.send_message(f"Insufficient funds. Your balance: ${balance}", ephemeral=True)
            return

        result = random.choice(['heads', 'tails'])
        if guess == result:
            new_balance = bank.update_balance(interaction.user.id, bet)
            await interaction.response.send_message(
                f"🎉 It was **{result}**! You won ${bet}. New balance: ${new_balance}"
            )
        else:
            new_balance = bank.update_balance(interaction.user.id, -bet)
            await interaction.response.send_message(
                f"😞 It was **{result}**. You lost ${bet}. New balance: ${new_balance}"
            )
