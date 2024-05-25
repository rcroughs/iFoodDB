import os


def clear():
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


class Colors:
    """
    Colors class to add colors to the CLI
    """

    @staticmethod
    def red(text: str) -> str:
        return f"\033[91m{text}\033[0m"

    @staticmethod
    def green(text: str) -> str:
        return f"\033[92m{text}\033[0m"

    @staticmethod
    def yellow(text: str) -> str:
        return f"\033[93m{text}\033[0m"

    @staticmethod
    def blue(text: str) -> str:
        return f"\033[94m{text}\033[0m"

    @staticmethod
    def purple(text: str) -> str:
        return f"\033[95m{text}\033[0m"

    @staticmethod
    def cyan(text: str) -> str:
        return f"\033[96m{text}\033[0m"

    @staticmethod
    def white(text: str) -> str:
        return f"\033[97m{text}\033[0m"

    @staticmethod
    def gray(text: str) -> str:
        return f"\033[90m{text}\033[0m"

    @staticmethod
    def black(text: str) -> str:
        return f"\033[30m{text}\033[0m"
