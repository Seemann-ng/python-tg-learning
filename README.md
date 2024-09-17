 # 🤖 Telegram quiz-bot for learning python 🤖

 ![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
 ![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
 ![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

> #### _My Telegram bot for python learning._

----

 ## 📠 Interaction with the bot: 📠

> ### ⌨️ _Commands:_ ⌨️
>
> ⏩ `/start` __- Start chat.__
> 
> ⏩ `/question` __- Get a question from the bot.__
> 
> 💡 ___Once the question is answered, bot will provide a link to the article on the topic of the question\
> by appending it to the message with the quiz.___
>
>> __⚠️ When one of the commands above is used, if there is an unanswered question in the chat,\
>> ⚠️ bot will forward this question instead of sending a new one.__
>
> ⏩ `/my_score` __- Show your score.__
> 
> ⏩ `/clear_my_score` __- Remove your score from the bot's memory.__
> 
> __⚠️ For debug purpose, there is also hidden `/clear` command,️ which removes all active questions sent to the User\
> ⚠️ from the bot's memory.__

----

 ## 🚢 Docker commands: 🚢

> ### 📝 _Build an image:_
>
> ⏩ `docker build . -t bot`

> ### 📦 _Build and run a new container:_
>
> ⏩ `docker run -d --restart always --name ilia-bot ilia-bot`

> ### ▶️ _Run the existing container:_
>
> ⏩ `docker start bot`

> ### ⏸ _Stop the container:_
>
> ⏩ `docker stop bot`

> ### 🗑  _Delete the container:_
>
> ⏩ `docker rm bot`
>
>> #### ⛔️ You have _NOT_ to delete an old _IMAGE_ when creating a new one with the same name. ⛔️
>>
>> #### ⚠️ You _HAVE TO DELETE_ an old _CONTAINER_ when creating a new one with the same name. ⚠️

> ### 🛂 _List of running containers:_ 🛂
>
> ⏩ `docker ps`

> ### 🛅 _List of all containers:_ 🛅
>
> ⏩ `docker ps -a`

> ### 🛃 _List of all images:_ 🛃
>
> ⏩ `docker image ls or docker images`
