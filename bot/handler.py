import json
from typing import List, Any, Dict

from tools import logger


class JSONHandler_:
    def __init__(self, filename):
        self.filename = filename

    def read(self) -> Any:
        """Read data from .json file and convert it to list or dictionary.

        Returns:
            Data from .json file.

        """
        with open(self.filename, "r", encoding="utf-8") as openfile:
            logger.info(f"Reading file {self.filename}.")
            readable_data = json.load(openfile)
            logger.info(f"Closing file {self.filename}.")
        return readable_data

    def write(self, written: List[Dict[str, str | int]] | Dict[str, str | int]) -> None:
        """Make or rewrite .json file containing data form given list or dictionary.

        Args:
            written: Data to be written into .json file.

        """
        with open(self.filename, "w", encoding="utf-8") as openjson:
            logger.info(f"Writing file {self.filename}.")
            json.dump(written, openjson, indent=4, ensure_ascii=False)
            logger.info(f"Closing file {self.filename}.")

    def list_append(self, added: Dict[str, str | int] | List[Dict[str, str | int]]) -> None:
        """Append given dictionary or list to given list-format .json file.

        Args:
            added: List or dictionary with data that is to be added to .json file.

        """
        logger.info("json_list_appender() enter.")
        json_being_changed: List[Any] = self.read()
        json_being_changed.append(added)
        self.write(json_being_changed)
        logger.info("json_list_appender() exit.")

    def dict_update(self, added: Dict[Any, Any]) -> None:
        """Update given dictionary-format .json with new key: value pairs.

        Args:
            added: Dictionary with data that is to be added to .json file.

        """
        logger.info("json_dict_updater() enter.")
        json_being_changed: Dict[str, Any] = self.read()
        json_being_changed.update(added)
        self.write(json_being_changed)
        logger.info("json_dict_updater() exit.")

    def dict_pop(self, popped: int | str) -> None:
        """Pop item from dictionary-format .json file.

        Args:
            popped: Key of item to be popped.

        """
        logger.info("json_dict_popper() enter.")
        json_being_changed = self.read()
        json_being_changed.pop(popped)
        self.write(json_being_changed)
        logger.info("json_dict_popper() exit.")
