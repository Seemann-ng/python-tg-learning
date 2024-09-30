from typing import Dict

WELCOME_MESSAGE = "Howdy, ready for some questions?"
SCORE_NOT_FOUND = "Sorry, You haven't been scored yet."
CLEAR_CHAT_HISTORY = "Your chat history has been cleared for the bot.\n(Your score hasn't been changed)"
CLEAR_SCORE = "Your score record has been removed."
WRONG_INPUT = f"Sorry, I can't understand that.\n" \
              f"Please use one of the following commands:\n" \
              f"/start to start the chat;\n" \
              f"/question to get a question from the bot;\n" \
              f"/my_score to get Your score;\n" \
              f"/clear to clear chat history for the bot;\n" \
              f"/clear_my_score to clear Your score for the bot."


def score_found(user_scores: Dict[str, int]) -> str:
    """Get message text with User's score.

    Args:
        user_scores: Dictionary of User's score.

    Returns:
        Message text with score.

    """
    score_message = f"Your score is {user_scores["correct"]} out of {user_scores["total"]} " \
                    f"({round(user_scores["correct"]/user_scores["total"] * 100)}%)."
    return score_message
