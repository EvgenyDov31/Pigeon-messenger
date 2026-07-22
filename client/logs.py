"""
Консольный месседжер

Модуль вывода сообщений и ошибок.
"""
VERSION = "0.3.7"

def print_error(text: str) -> None:
    """
    Вывод ошибок.
    """
    print(f"[Error]: {text}")


def print_notice(text: str) -> None:
    """
    Вывод оповещений.
    """
    print(f"[Notice]: {text}")


def print_client_help() -> None:
    """
    Вывод списка команд сервера.
    """
    help_message = f"""
        Pigeon client ver: {VERSION}

        Commands list:
        -----------------------------------------------
        1) "connect" : connect to server.
        2) "disconnect" : disconnect with server.
        3) "help" : show commands list.
        4) "send [user id] [message]" : send message to [user id] (without "[]").
        5) "exit" : exit the program.
        6) "loginStatus" : show login status.
        7) "login [user id] [password]" : log in to accaunt.
        8) "logout" : log out.
        9) "registration" : registration new accaunt.
        10) "changePassword" : change accaunt password.
        11) "deleteAccaunt" : delete accaunt.
        12) "get" [parameter] : outputs the value of parameter.
        13) "set" [parameter] [value] : sets the value of the parameter.
    """
    print(help_message)


def print_hello() -> None:
    """
    Вывод приветствия.
    """
    RESET = "\033[0m"
    GRAY = "\033[90m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"

    hello = rf"""
    {YELLOW}========================================================{RESET}
    {GRAY}========================================================{RESET}
    {CYAN}             ____  _
                |  _ \(_) __ _  ___  ___  _ __
                | |_) | |/ _` |/ _ \/ _ \| '_ \
                |  __/| | (_| |  __/ (_) | | | |
                |_|   |_| \__,|\___|\___/|_| |_|
                        |___/{RESET}
    {GRAY}========================================================{RESET}
    {YELLOW}========================================================{RESET}

    Pigeon Messenger Client

    Version : 0.3.7
    Author  : Evgeny Dov

    Type "help" for available commands.
    """
    print(hello)


def create_log(text: str) -> None:
    """
    Запись логов.
    """
    