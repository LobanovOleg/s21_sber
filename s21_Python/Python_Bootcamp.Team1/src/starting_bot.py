"""
These are instructions on how to run the bot on your device.\n
1) Launch the command prompt.
2) Go to the sloped directory in the src section.
3) Run the command “python3 -m venv .venv”.
4) Run the command “python3 -m pip install --upgrade pip”.
5) Run the command “python3 install -r requirements.txt”.
5+) If postgresql did not installed:
    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    psql -U postgres
    ALTER USER postgres WITH PASSWORD 'postgres';
6) Go to telegram, find BotFather and use it to generate a token for your bot.
7) In the .env file add “GAME_BOT_TOKEN=your_token”, where your_token should "
"be replaced by your generated token.
8) Execute the command “python3 game_bot.py”.
9) Find your created bot in Telegram.
10) Write to it “/start” and start playing.
"""
