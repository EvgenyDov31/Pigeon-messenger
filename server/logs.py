"""
Консольный месседжер

Модуль вывода сообщений и ошибок.
"""
VERSION = "0.4.1"

import os
from datetime import datetime

def print_error(text: str, err_text: str) -> None:
    """
    Вывод ошибок.
    """
    print(f"[Error]: {text}")
    create_log(text, log_type="error", err_text=err_text)


def print_notice(text: str) -> None:
    """
    Вывод оповещений.
    """
    print(f"[Notice]: {text}")
    create_log(text, log_type="info")


def print_clients_list_help_message() -> None:
    """
    Вывод списка команд для вывода списка клиентов.
    """
    help_message = """
        clients [argv]
        default: [--connected]
        arguments list:
        -----------------------------------------------
        1) [-c / --connected] : show connected clients list.
        2) [-h / --help] : show arguments list.
    """
    print(help_message)


def print_kick_help_message() -> None:
    """
    Вывод списка команд для команды "kick".
    """
    help_message = """
        kick [user_id] [argv]
        
        arguments list:
        -----------------------------------------------
        1) [-m / --message] [message] : kick user with sending message.
        2) [-nm / --nomessage] : kick user without message
        3) [-h / --help] : show arguments list.
    """
    print(help_message)


def print_start_server_help() -> None:
    """
    Вывод списка команд для запуска сервера.
    """
    help_message = """
        start [argv] 
        default: [--noaccept]
        arguments list:
        -----------------------------------------------
        1) [-a / --accept] : start server with clients accepting.
        2) [-na / --noaccept] : start server without clients accepting
        2) [-h / --help] : show arguments list.
    """
    print(help_message)


def print_server_help() -> None:
    """
    Вывод списка команд сервера.
    """
    help_message = f"""
        Pigeon server ver: {VERSION}\n
        Commands list:
        -----------------------------------------------
        1) "start [argv]" : start the server.
        2) "stop" : stop the server.
        3) "help" : show commands list.
        4) "exit" : exit the program.
        5) "clients [argv]" : show clients list
        6) "staccept" : start accepting clients
    """
    print(help_message)


def create_log(text: str, log_type="info", err_text="") -> None:
    """
    Запись логов.
    Принимает текст лога и его тип.
    type: 
    1) info - Общая информация, события и уведомления
    2) error - Информация, связанная с ошибками
    """
    if log_type.lower() == "info":
        log_type = "[INFO]: "
    
    elif log_type.lower() == "error":
        log_type = "[ERROR]: "
    
    else:
        return

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/logs.txt", "a") as file:
        if err_text:
            file.write(
                f"[{timestamp}] {log_type}{text}\n"
                f"Details: {err_text}\n"
            )
        else:
            file.write(
                f"[{timestamp}] {log_type}{text}\n"
            )