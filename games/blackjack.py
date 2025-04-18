
import random
import discord
from discord import app_commands
from discord.ui import View, Button

def setup_blackjack(tree, bank):
    @tree.command(name="blackjack", description="Play a game of blackjack")
    async def blackjack(interaction: discord.Interaction, bet: int):
        balance = bank.get_balance(interaction.user.id)
        if bet > balance or bet <= 0:
            await interaction.response.send_message(
                f"You can't bet ${bet}. Your balance is ${balance}.", ephemeral=True)
            return

        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        random.shuffle(deck)

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        def hand_value(hand):
            total = sum(hand)
            while total > 21 and 11 in hand:
                hand[hand.index(11)] = 1
                total = sum(hand)
            return total

        class BlackjackView(View):
            def __init__(self):
                super().__init__(timeout=60)
                self.player_hand = player_hand
                self.dealer_hand = dealer_hand
                self.deck = deck
                self.result = None

            async def interaction_check(self, i: discord.Interaction) -> bool:
                return i.user.id == interaction.user.id

            def get_embed(self):
                return discord.Embed(
                    title="🃏 Blackjack",
                    description=(
                        f"**Your hand:** {self.player_hand} (Total: {hand_value(self.player_hand)})\n"
                        f"**Dealer shows:** {self.dealer_hand[0]}"
                    ),
                    color=discord.Color.green()
                )

            @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
            async def hit(self, i: discord.Interaction, button: Button):
                self.player_hand.append(self.deck.pop())
                if hand_value(self.player_hand) > 21:
                    bank.update_balance(interaction.user.id, -bet)
                    embed = discord.Embed(
                        title="💥 Busted!",
                        description=f"You busted with {self.player_hand} (Total: {hand_value(self.player_hand)}).\nYou lose ${bet}.",
                        color=discord.Color.red()
                    )
                    await i.response.edit_message(embed=embed, view=None)
                    self.stop()
                else:
                    await i.response.edit_message(embed=self.get_embed(), view=self)

            @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary)
            async def stand(self, i: discord.Interaction, button: Button):
                while hand_value(self.dealer_hand) < 17:
                    self.dealer_hand.append(self.deck.pop())

                player_total = hand_value(self.player_hand)
                dealer_total = hand_value(self.dealer_hand)

                if dealer_total > 21 or player_total > dealer_total:
                    bank.update_balance(interaction.user.id, bet)
                    outcome = f"🎉 You win ${bet}!"
                    color = discord.Color.green()
                elif dealer_total > player_total:
                    bank.update_balance(interaction.user.id, -bet)
                    outcome = f"😞 You lose ${bet}."
                    color = discord.Color.red()
                else:
                    outcome = "It's a tie!"
                    color = discord.Color.blurple()

                embed = discord.Embed(
                    title="🃏 Final Hands",
                    description=(
                        f"**Your hand:** {self.player_hand} (Total: {player_total})\n"
                        f"**Dealer hand:** {self.dealer_hand} (Total: {dealer_total})\n\n{outcome}"
                    ),
                    color=color
                )
                await i.response.edit_message(embed=embed, view=None)
                self.stop()

        view = BlackjackView()
        await interaction.response.send_message(embed=view.get_embed(), view=view)
