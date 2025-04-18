
import discord
from discord import app_commands
import random
import math

active_games = {}

def calculate_multiplier(total_tiles, safe_reveals, mines):
    if safe_reveals == 0:
        return 1.0  # Starting multiplier
    safe_tiles = total_tiles - mines
    chance = 1.0
    for i in range(safe_reveals):
        chance *= (safe_tiles - i) / (total_tiles - i)
    house_edge = 0.99  # 1% house edge like Stake
    payout = (1 / chance) * house_edge
    return payout

class MinesGame:
    def __init__(self, bet, mines):
        self.bet = bet
        self.mines = mines
        self.board = ["⬜" for _ in range(25)]
        self.revealed = set()
        self.mine_indices = set(random.sample(range(25), mines))
        self.alive = True
        self.total_tiles = 25
        self.multiplier = 1.0

    def reveal_tile(self, index):
        if index in self.revealed or not self.alive:
            return False, None

        self.revealed.add(index)

        if index in self.mine_indices:
            self.board[index] = "💥"
            self.alive = False
            return True, "lose"
        else:
            self.board[index] = "💎"
            self.multiplier = calculate_multiplier(self.total_tiles, len(self.revealed), self.mines)
            return True, "safe"

    def cashout(self):
        return round(self.bet * self.multiplier)

class MinesView(discord.ui.View):
    def __init__(self, user_id, game, bank):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.game = game
        self.bank = bank
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for i in range(25):
            label = str(i + 1)
            style = discord.ButtonStyle.secondary
            disabled = False

            if i in self.game.revealed:
                if i in self.game.mine_indices:
                    label = "💥"
                    style = discord.ButtonStyle.danger
                else:
                    label = "💎"
                    style = discord.ButtonStyle.success
                disabled = True
            elif not self.game.alive:
                if i in self.game.mine_indices:
                    label = "💥"
                    style = discord.ButtonStyle.danger
                disabled = True

            self.add_item(MinesButton(index=i, label=label, style=style, disabled=disabled, bank=self.bank, game=self.game, user_id=self.user_id))

class MinesButton(discord.ui.Button):
    def __init__(self, index, label, style, disabled, bank, game, user_id):
        super().__init__(label=label, style=style, row=index // 5, disabled=disabled)
        self.index = index
        self.bank = bank
        self.game = game
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message('❌ This is not your game!', ephemeral=True)
            return
        if not self.game or not self.game.alive:
            await interaction.response.send_message("You're not in an active game.", ephemeral=True)
            return

        success, result = self.game.reveal_tile(self.index)
        if not success:
            await interaction.response.send_message("Already revealed or game over.", ephemeral=True)
            return

        view = MinesView(self.user_id, self.game, self.bank)
        if result == "lose":
            del active_games[self.user_id]
            embed = discord.Embed(title="💥 You hit a mine!", color=discord.Color.red())
        else:
            embed = discord.Embed(title="💎 Safe!", color=discord.Color.green())
            embed.set_footer(text=f"Multiplier: x{self.game.multiplier:.2f} • /cashout available")

        await interaction.response.edit_message(embed=embed, view=view)

def setup_mines(tree, bank):
    @tree.command(name="mines", description="Play a Stake-style Mines game")
    @app_commands.describe(bet="Amount to wager", mines="Number of mines (1-24)")
    async def mines(interaction: discord.Interaction, bet: int, mines: int):
        user_id = interaction.user.id

        if mines < 1 or mines >= 25:
            await interaction.response.send_message("Mines must be between 1 and 24.", ephemeral=True)
            return

        if active_games.get(user_id):
            await interaction.response.send_message("You already have an active game.", ephemeral=True)
            return

        balance = bank.get_balance(user_id)
        if bet > balance or bet <= 0:
            await interaction.response.send_message("Invalid bet amount.", ephemeral=True)
            return

        bank.update_balance(user_id, -bet)
        game = MinesGame(bet, mines)
        active_games[user_id] = game

        view = MinesView(user_id, game, bank)
        embed = discord.Embed(
            title="🧨 Mines Started",
            description="Click tiles to reveal. Avoid the mines!",
            color=discord.Color.dark_gold()
        )
        embed.set_footer(text="Use the buttons to reveal tiles. /cashout anytime.")
        await interaction.response.send_message(embed=embed, view=view)

    @tree.command(name="cashout", description="Cash out of your mines game")
    async def cashout(interaction: discord.Interaction):
        user_id = interaction.user.id
        game = active_games.get(user_id)

        if not game or not game.alive:
            await interaction.response.send_message("You're not in an active game.", ephemeral=True)
            return

        payout = game.cashout()
        bank.update_balance(user_id, payout)
        del active_games[user_id]

        embed = discord.Embed(
            title="💰 Cashed Out!",
            description=f"You won ${payout} with a multiplier of x{game.multiplier:.2f}",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
