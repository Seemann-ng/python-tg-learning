import json
import logging
import random
import time
from typing import List

import telebot
import telebot.types as types

import credentials

bot = telebot.TeleBot(credentials.BOT_TOKEN, parse_mode=None)
logging.basicConfig(
    filename="log.txt",
    filemode="w",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class JSONHandler_:
    @staticmethod
    def json_reader(filename: str) -> List[dict[str: str or int]] or dict[str: str or int]:
        """Read data from .json file and convert it to list or dictionary.

        Args:
            filename: Name of .json file to read.

        Returns:
            Data from .json file.

        """
        with open(filename, "r", encoding="utf-8") as openfile:
            readable_data = json.load(openfile)
        return readable_data

    @staticmethod
    def json_writer(filename: str, written: List[dict[str: str or int]] or dict[str: str or int]):
        """Make or rewrite .json file containing data form given list or dictionary.

        Args:
            filename: Name of .json file to write in.
            written: Data to be written into .json file.

        Returns:
            None.

        """
        with open(filename, "w", encoding="utf-8") as openjson:
            json.dump(written, openjson, indent=4, ensure_ascii=False)

    @staticmethod
    def json_list_appender(file_changed: str, added: dict[str: str or int] or List[dict[str: str or int]]):
        """Append given dictionary or list to given list-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            added: List or dictionary with data that is to be added to .json file.

        Returns:
            None.

        """
        json_being_changed: List[dict[str: str or int]] = JSONHandler_.json_reader(file_changed)
        json_being_changed.append(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_updater(file_changed: str, added: dict[str: str or int]):
        """Update given dictionary-format .json with new key: value pairs.

        Args:
            file_changed: Name of .json file to be modified.
            added: Dictionary with data that is to be added to .json file.

        Returns:
            None.

        """
        json_being_changed: dict[str: str or int] = JSONHandler_.json_reader(file_changed)
        json_being_changed.update(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_popper(file_changed: str, popped: str):
        """Pop item from dictionary-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            popped: Key of item to be popped.

        Returns:
            None.

        """
        json_being_changed: dict[str: str or int] = JSONHandler_.json_reader(file_changed)
        json_being_changed.pop(popped)
        JSONHandler_.json_writer(file_changed, json_being_changed)


questions = JSONHandler_.json_reader("questions.json")


def active_polls_checker(usr_id: int) -> dict[str: int] or False:
    """Check if there is any active quiz with this user.

    Args:
        usr_id: User or chat ID.

    Returns:
        Dict of poll IDs of active quizzes with user as keys and their message IDs as values, or False if there isn't any.

    """
    active_polls = JSONHandler_.json_reader("active_polls.json")
    poll_ids = dict()
    for poll in active_polls:
        if active_polls[poll]["user_id"] == usr_id:
            poll_ids.update({poll: active_polls[poll]["message_id"]})
    if not poll_ids:
        return False
    else:
        return poll_ids


def send_quiz(cid):
    """Send quiz-type poll to user; update active_polls.json adding info about poll, message and user IDs,
    correct option index and link to article on the topic of the quiz.

    Args:
        cid: Chat ID of the chat with user.

    Returns:
        None.

    """
    bot.send_chat_action(cid, "typing")
    time.sleep(0.5)
    question_number = random.randint(0, len(questions) - 1)
    answer_options_list = [option for option in questions[question_number]["answer_options"]]
    random.shuffle(answer_options_list)
    answer_options = [types.InputPollOption(option) for option in answer_options_list]
    poll: telebot.types.Message = bot.send_poll(
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
    JSONHandler_.json_dict_updater("active_polls.json", poll_info)
    logging.info(f"Poll {poll.json["poll"]["id"]} has been opened.")


@bot.message_handler(commands=["start"])
def start_command(message):
    """Start chat with user by sending them welcome message and a poll once /start command received.

    Args:
        message: Message from User with /start command in it.

    Returns:
        None.

    """
    logging.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    logging.info(f"New chat with user {message.from_user.username} (id {message.from_user.id}) has been started.")
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Howdy, ready for some questions?")
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
def my_score_command(message):
    """Tell user their score in X-out-of-Y format or inform them they aren't scored yet.

    Args:
        message: Message from User with /my_score command in it.

    Returns:
        None.

    """
    logging.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    logging.info(f"User {message.from_user.username} (id {message.from_user.id}) requested their score.")
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.5)

    if str(message.from_user.id) in list(JSONHandler_.json_reader("scores.json"))[:]:
        user_scores = JSONHandler_.json_reader("scores.json")[str(message.from_user.id)]
        bot.send_message(
            message.chat.id,
            f"Your score is {user_scores["correct"]} out of {user_scores["total"]} "
            f"({round(user_scores["correct"]/user_scores["total"] * 100)}%)."
        )
        logging.info(f"Score request for user ID {message.from_user.id} succeed.")
    else:
        bot.send_message(message.chat.id, "Sorry, You haven't been scored yet.")
        logging.info(f"Score entry {message.from_user.id} wasn't found.")


@bot.message_handler(commands=["question"])
def question_command(message):
    """Send user a poll once the /question command is received if there is no active one; or forward
    existing active poll to User.

    Args:
        message: Message from User with /question command in it.

    Returns:
        None.

    """
    logging.info(
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
def clear_command(message):
    """Remove info about active polls related to User from active_polls.json.

    Args:
        message: Message from User with /clear command in it.

    Returns:
        None.

    """
    logging.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    active_polls = active_polls_checker(message.chat.id)
    if active_polls:
        for poll in active_polls:
            JSONHandler_.json_dict_popper("active_polls.json", poll)
            logging.info(f"Poll {poll} has been removed from active_polls.json.")
    bot.send_message(
        message.chat.id,
        "Your chat history has been cleared for the bot.\n(Your score hasn't been changed)"
    )
    logging.info(f"Active polls have been cleared for user {message.from_user.id} (id {message.chat.id}).")


@bot.message_handler(commands=["clear_my_score"])
def clear_my_score_command(message):
    """Remove score entry of User from scores.json.

    Args:
        message: Message from User with /clear_my_score command in it.

    Returns:
        None.

    """
    logging.info(
        f"\"{message.text}\" command from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    if str(message.from_user.id) in list(JSONHandler_.json_reader("scores.json"))[:]:
        JSONHandler_.json_dict_popper("scores.json", str(message.from_user.id))
    bot.send_message(message.chat.id, "Your score record has been removed.")
    logging.info(f"Score record for user {message.from_user.username} (id {message.from_user.id}) has been removed.")


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer: types.PollAnswer):
    """Update scores.json file with new scores and send new poll to the user if there is no active one; or forward
    existing active poll to User.

    Args:
        poll_answer: Poll answer from user.

    Returns:
        None.

    """
    doc_link = JSONHandler_.json_reader("active_polls.json")[str(poll_answer.poll_id)]["doc_link"]
    """Providing article link to User.
    
    """
    if doc_link:
        logging.info(f"Documentation link is being provided to User.")
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        article = types.InlineKeyboardButton(text="Article", url=doc_link)
        markup.add(article)
        bot.edit_message_reply_markup(
            chat_id=poll_answer.user.id,
            message_id=JSONHandler_.json_reader("active_polls.json")[str(poll_answer.poll_id)]["message_id"],
            reply_markup=markup
        )
        logging.info(f"Documentation link has been provided to User.")

    logging.info(f"User {poll_answer.user.username} (id {poll_answer.user.id}) answered {poll_answer.option_ids[0]}.")
    initial_user_score = {
        poll_answer.user.id: {
            "correct": 0,
            "total": 0
        }
    }

    scores: dict[str: List[int]] = JSONHandler_.json_reader("scores.json")
    """Checking weather the entry about the user is absent in scores.json and make a new entry if so.
        
    """
    if str(poll_answer.user.id) not in list(scores)[:]:
        JSONHandler_.json_dict_updater("scores.json", initial_user_score)
        logging.info(f"New user entry \"{poll_answer.user.id}\" has been added to the scores.json.")
        scores = JSONHandler_.json_reader("scores.json")

    if poll_answer.option_ids[0] == JSONHandler_.json_reader("active_polls.json")[str(poll_answer.poll_id)]["correct_op_id"]:
        """Checking if the answer is correct and update scores variable accordingly.
        
        """
        scores[str(poll_answer.user.id)]["correct"] += 1
        scores[str(poll_answer.user.id)]["total"] += 1
    elif poll_answer.option_ids[0] != JSONHandler_.json_reader("active_polls.json")[str(poll_answer.poll_id)]["correct_op_id"]:
        scores[str(poll_answer.user.id)]["total"] += 1

    JSONHandler_.json_dict_updater("scores.json", scores)
    """Update scores.json file.
    
    """
    logging.info(f"User score for entry \"{poll_answer.user.id}\" has been updated.")

    logging.info(f"Active poll {poll_answer.poll_id} is being closed.")
    """Deleting info about current poll from active_polls.json file.
    
    """
    JSONHandler_.json_dict_popper("active_polls.json", poll_answer.poll_id)
    logging.info(f"Poll has been closed.")
    bot.send_chat_action(poll_answer.user.id, 'typing')
    time.sleep(0.5)

    active_poll = active_polls_checker(poll_answer.user.id)
    """Checking if there is any active poll.
    
    """
    if active_poll:
        bot.forward_message(
            poll_answer.user.id,
            poll_answer.user.id,
            active_poll[list(active_poll)[0]]
        )
    else:
        send_quiz(poll_answer.user.id)


@bot.message_handler(content_types=["poll"])
def add_question_to_json(message):
    """Add new poll info from received poll-type message to the questions.json file.

    Args:
        message: Received poll-type message.

    Returns:
        None.

    """
    question = {
        "question": message.poll.question,
        "answer_options": [option.text for option in message.poll.options],
        "correct_option": message.poll.options[message.poll.correct_option_id].text,
        "explanation": message.poll.explanation,
        "doc_link": 0
    }
    JSONHandler_.json_list_appender("questions.json", question)
    logging.info("New question added to the question.json file.")


@bot.message_handler(func=lambda message: True)
def non_command(message):
    """Handle non-command message with sending a message to User.

    Args:
        message: Message from User with no command in it.

    Returns:
        None.

    """
    logging.info(
        f"\"{message.text}\" message from user {message.from_user.username}"
        f"(id {message.from_user.id}) has been received."
    )
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(0.5)
    bot.send_message(
        message.chat.id,
        f"Sorry, I can't understand that.\n"
        f"Please use one of the following commands:\n"
        f"/start to start the chat;\n"
        f"/question to get a question from the bot;\n"
        f"/my_score to get Your score;\n"
        # f"/clear to clear chat history for the bot;\n"
        f"/clear_my_score to clear Your score for the bot."
    )


def main():
    logging.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
