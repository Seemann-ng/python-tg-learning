import random
import time
from typing import Dict

import telebot
import telebot.types as types
from environs import Env

import botmessages
from tools import logger
from jsonhandler import JSONHandler_ as JSONHandler

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


def active_polls_checker(usr_id: int) -> Dict[str, int] | False:
    """Check if there is any active quiz with this user.

    Args:
        usr_id: User or chat ID.

    Returns:
        Dict of poll IDs of active quizzes with user as keys and their message IDs as values, or False if there isn't any.

    """
    active_polls = JSONHandler.read("active_polls.json")
    poll_ids = {}
    for poll in active_polls:
        if active_polls[poll]["user_id"] == usr_id:
            poll_ids.update({poll: active_polls[poll]["message_id"]})
    return poll_ids or False


def send_quiz(cid: int) -> None:
    """Send quiz-type poll to user; update active_polls.json adding info about poll, message and user IDs,
    correct option index and link to article on the topic of the quiz.

    Args:
        cid: Chat ID of the chat with user.

    """
    bot.send_chat_action(cid, "typing")
    time.sleep(0.3)
    questions = JSONHandler.read("questions.json")
    question_number = random.randint(0, len(questions) - 1)
    answer_options_list = [option for option in questions[question_number]["answer_options"]]
    random.shuffle(answer_options_list)
    answer_options = [types.InputPollOption(option) for option in answer_options_list]
    poll = bot.send_poll(
        chat_id=cid,
        question=questions[question_number]["question"],
        options=answer_options,
        type="quiz",
        correct_option_id=answer_options_list.index(questions[question_number]["correct_option"]),
        is_anonymous=False,
        explanation=questions[question_number]["explanation"]
    )
    poll_info = {
        poll.json["poll"]["id"]: {
            "user_id": poll.json["chat"]["id"],
            "correct_op_id": poll.json["poll"]["correct_option_id"],
            "message_id": poll.json["message_id"],
            "doc_link": questions[question_number]["doc_link"]
        }
    }
    JSONHandler.dict_update("active_polls.json", poll_info)
    logger.info(f"Poll {poll.json["poll"]["id"]} has been opened.")


@bot.message_handler(commands=["start"])
def start_command(message: types.Message) -> None:
    """Start chat with user by sending them welcome message and a poll once /start command received.

    Args:
        message: Message from User with /start command in it.

    """
    logger.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    logger.info(f"New chat with user {message.from_user.username} (id {message.from_user.id}) has been started.")
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.3)
    bot.send_message(message.chat.id, botmessages.WELCOME_MESSAGE)
    active_poll = active_polls_checker(message.chat.id)
    if active_poll:
        bot.forward_message(
            message.chat.id,
            message.chat.id,
            active_poll[list(active_poll)[0]]
        )
    else:
        send_quiz(message.chat.id)


@bot.message_handler(commands=["my_score"])
def my_score_command(message: types.Message) -> None:
    """Tell user their score in X-out-of-Y format or inform them they aren't scored yet.

    Args:
        message: Message from User with /my_score command in it.

    """
    logger.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    logger.info(f"User {message.from_user.username} (id {message.from_user.id}) requested their score.")
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.5)

    if str(message.from_user.id) in list(JSONHandler.read("scores.json"))[:]:
        user_scores = JSONHandler.read("scores.json")[str(message.from_user.id)]
        bot.send_message(message.chat.id, botmessages.score_found(user_scores))
        logger.info(f"Score request for user ID {message.from_user.id} succeed.")
    else:
        bot.send_message(message.chat.id, botmessages.SCORE_NOT_FOUND)
        logger.info(f"Score entry {message.from_user.id} wasn't found.")


@bot.message_handler(commands=["question"])
def question_command(message: types.Message) -> None:
    """Send user a poll once the /question command is received if there is no active one; or forward
    existing active poll to User.

    Args:
        message: Message from User with /question command in it.

    """
    logger.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    active_poll = active_polls_checker(message.chat.id)
    if active_poll:
        bot.forward_message(
            message.chat.id,
            message.chat.id,
            active_poll[list(active_poll)[0]]
        )
    else:
        send_quiz(message.chat.id)


@bot.message_handler(commands=["clear"])
def clear_command(message: types.Message) -> None:
    """Remove info about active polls related to User from active_polls.json.

    Args:
        message: Message from User with /clear command in it.

    """
    logger.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    active_polls = active_polls_checker(message.chat.id)
    if active_polls:
        for poll in active_polls:
            JSONHandler.dict_pop("active_polls.json", poll)
            logger.info(f"Poll {poll} has been removed from active_polls.json.")
    bot.send_message(message.chat.id, botmessages.CLEAR_CHAT_HISTORY)
    logger.info(f"Active polls have been cleared for user {message.from_user.id} (id {message.chat.id}).")


@bot.message_handler(commands=["clear_my_score"])
def clear_my_score_command(message: types.Message) -> None:
    """Remove score entry of User from scores.json.

    Args:
        message: Message from User with /clear_my_score command in it.

    """
    logger.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    if str(message.from_user.id) in list(JSONHandler.read("scores.json"))[:]:
        JSONHandler.dict_pop("scores.json", str(message.from_user.id))
    bot.send_message(message.chat.id, botmessages.CLEAR_SCORE)
    logger.info(f"Score record for user {message.from_user.username} (id {message.from_user.id}) has been removed.")


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer: types.PollAnswer) -> None:
    """Update scores.json file with new scores and send new poll to the user if there is no active one; or forward
    existing active poll to User.

    Args:
        poll_answer: Poll answer from user.

    """
    # Providing article link to User.
    doc_link = JSONHandler.read("active_polls.json")[str(poll_answer.poll_id)]["doc_link"]
    if doc_link:
        logger.info(f"Documentation link is being provided to User.")
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        article = types.InlineKeyboardButton(text="Article", url=doc_link)
        markup.add(article)
        bot.edit_message_reply_markup(
            chat_id=poll_answer.user.id,
            message_id=JSONHandler.read("active_polls.json")[str(poll_answer.poll_id)]["message_id"],
            reply_markup=markup
        )
        logger.info(f"Documentation link has been provided to User.")

    logger.info(f"User {poll_answer.user.username} (id {poll_answer.user.id}) answered {poll_answer.option_ids[0]}.")
    initial_user_score = {
        str(poll_answer.user.id): {
            "correct": 0,
            "total": 0
        }
    }

    # Checking weather the entry about the user is absent in scores.json and make a new entry if so.
    scores: Dict[str, Dict[str, int]] = JSONHandler.read("scores.json")
    if str(poll_answer.user.id) not in list(scores)[:]:
        JSONHandler.dict_update("scores.json", initial_user_score)
        logger.info(f"New user entry \"{poll_answer.user.id}\" has been added to the scores.json.")
        scores = JSONHandler.read("scores.json")

    # Checking if the answer is correct and update scores variable accordingly.
    correct_answer = JSONHandler.read("active_polls.json")[str(poll_answer.poll_id)]["correct_op_id"]
    if poll_answer.option_ids[0] == correct_answer:
        scores[str(poll_answer.user.id)]["correct"] += 1
        scores[str(poll_answer.user.id)]["total"] += 1
    elif poll_answer.option_ids[0] != correct_answer:
        scores[str(poll_answer.user.id)]["total"] += 1

    # Update scores.json file.
    JSONHandler.dict_update("scores.json", scores)
    logger.info(f"User score for entry \"{poll_answer.user.id}\" has been updated.")

    # Deleting info about current poll from active_polls.json file.
    logger.info(f"Active poll {poll_answer.poll_id} is being closed.")
    JSONHandler.dict_pop("active_polls.json", poll_answer.poll_id)
    logger.info(f"Poll has been closed.")
    bot.send_chat_action(poll_answer.user.id, 'typing')
    time.sleep(0.5)
    
    # Checking if there is any active poll.
    active_poll = active_polls_checker(poll_answer.user.id)
    if active_poll:
        bot.forward_message(poll_answer.user.id, poll_answer.user.id, active_poll[list(active_poll)[0]])
    else:
        send_quiz(poll_answer.user.id)


@bot.message_handler(content_types=["poll"])
def append_question(message) -> None:
    """Add new poll info from received poll-type message to the questions.json file.

    Args:
        message: Received poll-type message.

    """
    question = {
        "question": message.poll.question,
        "answer_options": [option.text for option in message.poll.options],
        "correct_option": message.poll.options[message.poll.correct_option_id].text,
        "explanation": message.poll.explanation,
        "doc_link": 0
    }
    JSONHandler.list_append("questions.json", question)
    logger.info("New question added to the question.json file.")


@bot.message_handler(func=lambda message: True)
def non_command(message: types.Message) -> None:
    """Handle non-command message with sending a message to User.

    Args:
        message: Message from User with no command in it.

    """
    logger.info(
        f"\"{message.text}\" message from user {message.from_user.username}"
        f"(id {message.from_user.id}) has been received."
    )
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.5)
    bot.send_message(message.chat.id, botmessages.WRONG_INPUT)


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
