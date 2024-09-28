import json
from typing import List, Any, Dict

from tools import logger


class JSONHandler_:
    @staticmethod
    def read(filename: str) -> Any:
        """Read data from .json file and convert it to list or dictionary.

        Args:
            filename: Name of .json file to read.

        Returns:
            Data from .json file.

        """
        with open(filename, "r", encoding="utf-8") as openfile:
            logger.info(f"Reading file {filename}.")
            readable_data = json.load(openfile)
            logger.info(f"Closing file {filename}.")
        return readable_data

    @staticmethod
    def write(filename: str, written: List[Dict[str, str | int]] | Dict[str, str | int]) -> None:
        """Make or rewrite .json file containing data form given list or dictionary.

        Args:
            filename: Name of .json file to write in.
            written: Data to be written into .json file.

        """
        with open(filename, "w", encoding="utf-8") as openjson:
            logger.info(f"Writing file {filename}.")
            json.dump(written, openjson, indent=4, ensure_ascii=False)
            logger.info(f"Closing file {filename}.")

    @staticmethod
    def list_append(file_changed: str, added: Dict[str, str | int] | List[Dict[str, str | int]]) -> None:
        """Append given dictionary or list to given list-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            added: List or dictionary with data that is to be added to .json file.

        """
        logger.info("json_list_appender() enter.")
        json_being_changed: List[Any] = JSONHandler_.read(file_changed)
        json_being_changed.append(added)
        JSONHandler_.write(file_changed, json_being_changed)
        logger.info("json_list_appender() exit.")

    @staticmethod
    def dict_update(file_changed: str, added: Dict[str, Any]) -> None:
        """Update given dictionary-format .json with new key: value pairs.

        Args:
            file_changed: Name of .json file to be modified.
            added: Dictionary with data that is to be added to .json file.

        """
        logger.info("json_dict_updater() enter.")
        json_being_changed: Dict[str, Any] = JSONHandler_.read(file_changed)
        json_being_changed.update(added)
        JSONHandler_.write(file_changed, json_being_changed)
        logger.info("json_dict_updater() exit.")

    @staticmethod
    def dict_pop(file_changed: str, popped: str) -> None:
        """Pop item from dictionary-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            popped: Key of item to be popped.

        """
        logger.info("json_dict_popper() enter.")
        json_being_changed: Dict[str, Any] = JSONHandler_.read(file_changed)
        json_being_changed.pop(popped)
        JSONHandler_.write(file_changed, json_being_changed)
        logger.info("json_dict_popper() exit.")
