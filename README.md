
# Discord Gambling Bot

This is a chill little Discord bot made with Python. It lets you gamble fake money with your friends using slash commands. Classic stuff like coin flips and blackjack, all wrapped up in a simple interface.

---

## What it does

- Tracks user balances in a JSON file (yep, just a simple file — no database needed)
- `/coinflip` lets you bet on heads or tails
- `/blackjack` gives you a basic blackjack game against a virtual dealer
- All commands are slash commands, so you can just type `/` and pick what you want

---

## Getting Started

1. Clone the repo:

```bash
git clone https://github.com/your-username/discord-gambler.git
cd discord-gambler
```

2. Install what you need:

```bash
pip install -r requirements.txt
```

3. Put your bot token into `main.py` (where it says `YOUR_DISCORD_BOT_TOKEN`)

4. Run the bot:

```bash
python main.py
```

---

## Folder Breakdown

```
discord-gambler/
├── main.py             # Starts the bot
├── bank.py             # Keeps track of balances
├── games/
│   ├── coinflip.py     # Coin flip logic
│   └── blackjack.py    # Blackjack logic
├── data/
│   └── bank.json       # Stores user money
├── requirements.txt    # Dependencies
└── README.md           # You're reading it
```

---

## Might Add Later

- Command to check your balance
- Leaderboard to see who’s rich
- More games (slots? roulette?)
- Better storage (like SQLite or MongoDB maybe for global leaderboards)

---

## Final Thoughts

This is just a fun little side project. If you want to expand on it or tweak the rules, go for it.

Have fun, and maybe don’t bet your rent money... even if it’s fake.
