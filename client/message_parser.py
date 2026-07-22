"""
Консольный месседжер

Модуль парсинга сообщений сервера.
"""

import json
from message_types import TYPE_SEND, TYPE_LOGIN, TYPE_REGISTR, TYPE_DELETE_USER, TYPE_CHANGE_PASSWORD, TYPE_LOGOUT, TYPE_KICK
import logs

def print_message(packet: dict, client) -> None:
    """
    Формирует json и отправляет сообщение.
    """
    message = packet["message"]
    from_user_id, from_username = packet["from"] # ID и имя получателя
    client.print_message(from_user_id, from_username, message) # Вывод сообщения сообщения


def message_parser(packet: dict, client) -> None:
    """
    Парсит сообщение сервера.
    Принимает полученый пакет (сообщение), IP отправителя, объект сервера
    """

    if packet["type"] == TYPE_SEND:
        print_message(packet, client)

    elif packet["type"] == TYPE_LOGIN:
        if packet["result"] == True:
            client.set_login(True)
            logs.print_notice("Login successful")
            print("> ", end="", flush=True)
        else:
            logs.print_notice("Wrong user id or password")
            print("> ", end="", flush=True)

    elif packet["type"] == TYPE_REGISTR:
        if packet["result"] == True:
            logs.print_notice("Registration successful")
            print("> ", end="", flush=True)
        else:
            logs.print_error("Couldn't registrate")
            print("> ", end="", flush=True)

    elif packet["type"] == TYPE_DELETE_USER:
        if packet["result"] == True:
            logs.print_notice("Deletion successful")
            print("> ", end="", flush=True)
        else:
            logs.print_error("Couldn't delete")
            print("> ", end="", flush=True)

    elif packet["type"] == TYPE_CHANGE_PASSWORD:
        if packet["result"] == True:
            logs.print_notice("Password has been successfully changed")
            print("> ", end="", flush=True)
        else:
            logs.print_error("Couldn't change password")
            print("> ", end="", flush=True)

    elif packet["type"] == TYPE_LOGOUT:
        if packet["result"] == True:
            logs.print_notice("You have logged out of your account")
            print("> ", end="", flush=True)
        else:
            logs.print_error("Couldn't logged out")
            print("> ", end="", flush=True)

    elif packet["type"] == TYPE_KICK:
        logs.print_notice(f"You have been logged out\n{packet["message"]}")
        client.set_login(False)
        print("> ", end="", flush=True)