﻿# My **new** Telegram Bot

## Used libraries:
+ [***Aiogram-2x***](https://aiogram.dev)
+ [***vk_api***](https://vk-api.readthedocs.io/en/latest/index.html)
+ [***requests***](https://pydocbrowser.github.io/requests/latest/)
+ [***sqlite3***](https://docs.python.org/3/library/sqlite3.html)

---

# How does the telegram bot get started:

```bash
user@DESKTOP GNU /PATH
$ cd ~

user@DESKTOP GNU ~
$ git clone https://github.com/omicron1catchme/tgbot

user@DESKTOP GNU ~
$ cd tgbot/

user@DESKTOP GNU ~/tgbot
$ cd create_bot/

user@DESKTOP GNU ~/tgbot
$ printf 'TOKEN="YOUR TELEGRAM BOT TOKEN API"' > telegram_token.py

user@DESKTOP GNU ~/tgbot/create_bot
$ python telegram_bot.py
Updates were skipped successfully.

Bot is running!
```

---

+ **tgbot/**
  + bot_handlers/
    + __init__.py
    + main_handlers.py
    + reg_handlers.py
    + states_handlers.py
  + create_bot/
    + createbot.py
    + telegram_bot.py
  + other/
    + database.py
    + imports.py
    + keyboards.py
    + states.py
    + VK_api.py
  + video/
    + bot_working.mp4
  + .gitignore
  + README.md
  + requirements.txt

---

# How to use it:

[***video about how the bot works***](https://github.com/omicron1catchme/tgbot/blob/main/video/bot_working.mp4)
