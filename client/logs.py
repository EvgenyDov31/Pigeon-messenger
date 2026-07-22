"""
Консольный месседжер

Модуль вывода сообщений и ошибок.
"""
VERSION = "0.3.5"

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


def create_log(text: str) -> None:
    """
    Запись логов.
    """
    