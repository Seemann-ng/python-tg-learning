import json
import random
import time
from typing import List

import telebot
import telebot.types as types

import credentials

bot = telebot.TeleBot(credentials.token, parse_mode=None)


class JSONHandler_:
    @staticmethod
    def json_reader(filename: str) -> List[dict[str: str or int]] or dict[str: str or int]:
        """
        Read data from .json file and convert it to list or dictionary.
        Args:
            filename: Name of .json file to read.

        Returns:
            Data from .json file.
        """
        with open(filename, 'r', encoding='utf-8') as openfile:
            readable_data = json.load(openfile)
        return readable_data

    @staticmethod
    def json_writer(filename: str, written: List[dict[str: str or int]] or dict[str: str or int]):
        """
        Make or rewrite .json file containing data form given list or dictionary.
        Args:
            filename: Name of .json file to write in.
            written: Data to be written into .json file.
        """
        with open(filename, 'w', encoding='utf-8') as openjson:
            json.dump(written, openjson, indent=4, ensure_ascii=False)

    @staticmethod
    def json_list_appender(file_changed: str, added: dict[str: str or int] or List[dict[str: str or int]]):
        """
        Append given dictionary or list to given list-format .json file.
        Args:
            file_changed: Name of .json file to be modified.
            added: List or dictionary with data that is to be added to .json file.
        """
        json_being_changed: List[dict[str: str or int]] = JSONHandler_.json_reader(file_changed)
        json_being_changed.append(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_updater(file_changed: str, added: dict[str: str or int]):
        """
        Update given dictionary-format .json with new key: value pairs.
        Args:
            file_changed: Name of .json file to be modified.
            added: Dictionary with data that is to be added to .json file.
        """
        json_being_changed: dict[str: str or int] = JSONHandler_.json_reader(file_changed)
        json_being_changed.update(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_popper(file_changed: str, popped: str):
        """
        Pop item from dictionary-format .json file.
        Args:
            file_changed: Name of .json file to be modified.
            popped: Key of item to be popped.
        """
        json_being_changed: dict[str: str or int] = JSONHandler_.json_reader(file_changed)
        json_being_changed.pop(popped)
        JSONHandler_.json_writer(file_changed, json_being_changed)


questions = JSONHandler_.json_reader("questions.json")


def send_poll(cid):
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
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
        poll.json["poll"]["id"]: poll.json["poll"]["correct_option_id"]
    }
    JSONHandler_.json_dict_updater("active_polls.json", poll_info)
    print(f"Poll {poll.json["poll"]["id"]} has been opened.")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"New chat with user {message.from_user.username} (id {message.from_user.id}) has been started")
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    bot.send_message(message.chat.id, "Howdy, ready for some questions?")
    send_poll(message.chat.id)


@bot.message_handler(commands=['myscore'])
def show_my_score(message):
    print(f"User {message.from_user.username} (id {message.from_user.id}) requested their score.")
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    if str(message.from_user.id) in list(JSONHandler_.json_reader("scores.json"))[:]:
        user_scores = JSONHandler_.json_reader("scores.json")[str(message.from_user.id)]
        bot.send_message(
            message.chat.id,
            f"Your score is {user_scores[0]} out of {user_scores[1]} which is {round(user_scores[0]/user_scores[1] * 100)}%"
        )
        print(f"Score request succeed.")
    else:
        bot.send_message(message.chat.id, "Sorry, You haven't been scored yet.")
        print(f"Score entry wasn't found.")


@bot.message_handler(commands=["question"])
def response_with_poll(message):
    print(
        f"Message: \"{message.text}\" from user {message.from_user.username} (id {message.from_user.id}) has been received."
    )
    send_poll(message.chat.id)


@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer: telebot.types.PollAnswer):
    print(f"User {pollAnswer.user.username} (id {pollAnswer.user.id}) answered {pollAnswer.option_ids[0]}")
    initial_user_score = {
        pollAnswer.user.id: [
            0,
            0
        ]
    }
    scores: dict[str: List[int]] = JSONHandler_.json_reader("scores.json")

    if str(pollAnswer.user.id) not in list(scores)[:]:
        JSONHandler_.json_dict_updater("scores.json", initial_user_score)
        print(f"New user entry \"{pollAnswer.user.id}\" has been added to the scores.json")
        scores = JSONHandler_.json_reader("scores.json")

    if pollAnswer.option_ids[0] == JSONHandler_.json_reader("active_polls.json")[str(pollAnswer.poll_id)]:
        scores[str(pollAnswer.user.id)][0] += 1
        scores[str(pollAnswer.user.id)][1] += 1
    elif pollAnswer.option_ids[0] != JSONHandler_.json_reader("active_polls.json")[str(pollAnswer.poll_id)]:
        scores[str(pollAnswer.user.id)][1] += 1

    JSONHandler_.json_dict_updater("scores.json", scores)
    print(f"User score for entry \"{pollAnswer.user.id}\" has been updated.")

    print(f"Active poll {pollAnswer.poll_id} is being closed.")
    JSONHandler_.json_dict_popper("active_polls.json", pollAnswer.poll_id)
    print(f"Poll has been closed.")
    bot.send_chat_action(pollAnswer.user.id, 'typing')
    time.sleep(1)
    send_poll(pollAnswer.user.id)


@bot.message_handler(content_types=["poll"])
def add_question_to_json(message):
    question = {
        "question": message.poll.question,
        "answer_options": [option.text for option in message.poll.options],
        "correct_option": message.poll.options[message.poll.correct_option_id].text,
        "explanation": message.poll.explanation
    }
    JSONHandler_.json_list_appender("questions.json", question)
    print("New question added to the question.json file.")


def main():
    print("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
