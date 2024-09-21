import json
from typing import List, Any, Dict


class JSONHandler_:
    @staticmethod
    def json_reader(filename: str) -> Any:
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
    def json_writer(filename: str, written: List[Dict[str, str | int]] | Dict[str, str | int]) -> None:
        """Make or rewrite .json file containing data form given list or dictionary.

        Args:
            filename: Name of .json file to write in.
            written: Data to be written into .json file.

        """
        with open(filename, "w", encoding="utf-8") as openjson:
            json.dump(written, openjson, indent=4, ensure_ascii=False)

    @staticmethod
    def json_list_appender(file_changed: str, added: Dict[str, str | int] | List[Dict[str, str | int]]) -> None:
        """Append given dictionary or list to given list-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            added: List or dictionary with data that is to be added to .json file.

        """
        json_being_changed: List[Any] = JSONHandler_.json_reader(file_changed)
        json_being_changed.append(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_updater(file_changed: str, added: Dict[str, Any]) -> None:
        """Update given dictionary-format .json with new key: value pairs.

        Args:
            file_changed: Name of .json file to be modified.
            added: Dictionary with data that is to be added to .json file.

        """
        json_being_changed: Dict[str, Any] = JSONHandler_.json_reader(file_changed)
        json_being_changed.update(added)
        JSONHandler_.json_writer(file_changed, json_being_changed)

    @staticmethod
    def json_dict_popper(file_changed: str, popped: str) -> None:
        """Pop item from dictionary-format .json file.

        Args:
            file_changed: Name of .json file to be modified.
            popped: Key of item to be popped.

        """
        json_being_changed: Dict[str, Any] = JSONHandler_.json_reader(file_changed)
        json_being_changed.pop(popped)
        JSONHandler_.json_writer(file_changed, json_being_changed)
