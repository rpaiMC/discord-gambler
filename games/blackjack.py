
import random
import discord

def setup_blackjack(tree, bank):
    @tree.command(name="blackjack", description="Play a game of blackjack")
    async def blackjack(interaction: discord.Interaction, bet: int):
        await interaction.response.defer()

        balance = bank.get_balance(interaction.user.id)
        if bet > balance or bet <= 0:
            await interaction.followup.send(f"Insufficient funds. Your balance: ${balance}", ephemeral=True)
            return

        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        random.shuffle(deck)

        def draw(hand): hand.append(deck.pop())

        player = []
        dealer = []
        draw(player)
        draw(player)
        draw(dealer)

        def value(hand):
            total = sum(hand)
            while total > 21 and 11 in hand:
                hand[hand.index(11)] = 1
                total = sum(hand)
            return total

        while True:
            val = value(player)
            if val > 21:
                bank.update_balance(interaction.user.id, -bet)
                await interaction.followup.send(f"You busted with {val}. You lose ${bet}.")
                return

            hand_str = f"Your hand: {player} (total: {val})
Dealer shows: {dealer[0]}"
            await interaction.followup.send(hand_str + "
Type `hit` or `stand`.")

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.lower() in ['hit', 'stand']

            msg = await interaction.client.wait_for('message', check=check)
            if msg.content.lower() == 'hit':
                draw(player)
            else:
                break

        while value(dealer) < 17:
            draw(dealer)

        p_val = value(player)
        d_val = value(dealer)
        result = f"Your hand: {player} ({p_val})\nDealer hand: {dealer} ({d_val})\n"

        if d_val > 21 or p_val > d_val:
            bank.update_balance(interaction.user.id, bet)
            result += f"🎉 You win ${bet}!"
        elif d_val > p_val:
            bank.update_balance(interaction.user.id, -bet)
            result += f"😞 You lose ${bet}."
        else:
            result += "It's a tie!"

        await interaction.followup.send(result)
