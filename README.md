
# Discord Gambling Bot

simple discord casino, has the following features:
- play blackjack
- coinflip
- check your balance

---


## What it does

- Tracks user balances in a JSON file
- `/coinflip` to bet on heads or tails
- `/blackjack` to play against the house
- `/daily` to claim $10,000 once a day
- `/bank` to check your balance
- `/money` (admin-only) to give or remove money
- `/slots` slot machine game with emoji reels and payouts

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
├── main.py                         # Starts the bot
├── bank.py                         # Keeps track of balances
├── games/
│   ├── coinflip.py                 # Coin flip logic
│   └── blackjack.py                # Blackjack logic
├── commands/
│   ├── economy.py                  # /daily and /bank
│   └── economy_extensions.py       # /money and /slots
├── data/
│   ├── bank.json                   # Stores user money
│   └── cooldowns.json              # Tracks daily cooldowns
├── requirements.txt                # Dependencies
└── README.md                       # You're reading it
```

---

## Might Add Later
- Slots
- Wallet and bank differentiation, and robbing mechanic
- fancier embeds

---

## credits

shout out to stackoverflow and chatgpt, and my girlfriend for feature testing


