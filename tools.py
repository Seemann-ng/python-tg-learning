import logging
import functools

from telebot import types

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("bot_logger")

def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(message: types.Message):
        logger.info(
            f"\"{message.text}\" command from user {message.from_user.username} ({message.from_user.id}) has been received."
        )
        return func(message)
    return wrapper