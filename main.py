from tools import secrets, bot


if __name__ == '__main__':
    bot = bot.bg_bot
    bot.run(secrets.token)
