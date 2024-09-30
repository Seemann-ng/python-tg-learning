# 🤖 Telegram quiz-bot for learning python

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

My Telegram bot for python learning.

Bot is available on https://t.me/Seemann_ng_bot

## 💾 Build and run:

Run the following command to start the bot:

```bash
docker compose up -d --build
```

## 🔐 Environment:

In the `.env` file, or through the `-e` flags, you must set the required variables from
tables below.

| Variable    | Default        | Description        |
|-------------|----------------|--------------------|
| `BOT_TOKEN` | **(required)** | Telegram bot token |

## 📠 Interaction with the bot:

### ⌨️ Commands:

`/start` - start chat.
 
`/question` - get a question from the bot.
 
💡 __Once the question is answered, bot will provide a link to the article on the topic of the question by appending it to the message with the quiz.__
 
__⚠️ When one of the commands above is used, if there is an unanswered question in the chat, bot will forward this question instead of sending a new one.__

`/my_score` - show your score.
 
`/clear_my_score` - remove your score from the bot's memory.

__⚠️ For debug purpose, there is hidden `/clear` command,️ which removes active questions sent to the User 
from the bot's memory.__

## 👨‍🔧Built with:

* [Python 3.12](https://www.python.org/) - programming language
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng)

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details
