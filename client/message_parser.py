"""
Консольный месседжер

Модуль парсинга сообщений сервера.
"""

from message_types import TYPE_SEND, TYPE_LOGIN, TYPE_REGISTR, TYPE_DELETE_USER, TYPE_CHANGE_PASSWORD, TYPE_LOGOUT, TYPE_KICK
import logs

def print_message(packet: dict, client) -> None:
    """
    Формирует json и отправляет сообщение.
    """
    message = packet["message"]
    sender = packet.get("from")

    if not isinstance(sender, tuple) or len(sender) != 2:
        logs.print_error("Invalid sender format")
        return

    from_user_id, from_username = sender

    client.print_message(from_user_id, from_username, message) 


def show_prompt():
    print("> ", end="", flush=True)


def message_parser(packet: dict, client) -> None:
    """
    Парсит сообщение сервера.
    Принимает полученый пакет (сообщение), IP отправителя, объект сервера
    """
    packet_type = packet.get("type")

    if packet_type is None:
        logs.print_error("Invalid packet: missing 'type'")
        return

    if packet["type"] == TYPE_SEND:
        print_message(packet, client)

    elif packet["type"] == TYPE_LOGIN:
        if packet.get("result") is True:
            client.set_login(True)
            logs.print_notice("Login successful")
            show_prompt()
        else:
            logs.print_notice("Wrong user id or password")
            show_prompt()

    elif packet["type"] == TYPE_REGISTR:
        if packet.get("result") is True:
            logs.print_notice("Registration successful")
            show_prompt()
        else:
            logs.print_error("Couldn't register")
            show_prompt()

    elif packet["type"] == TYPE_DELETE_USER:
        if packet.get("result") is True:
            logs.print_notice("Deletion successful")
            show_prompt()
        else:
            logs.print_error("Couldn't delete")
            show_prompt()

    elif packet["type"] == TYPE_CHANGE_PASSWORD:
        if packet.get("result") is True:
            logs.print_notice("Password has been successfully changed")
            show_prompt()
        else:
            logs.print_error("Couldn't change password")
            show_prompt()

    elif packet["type"] == TYPE_LOGOUT:
        if packet.get("result") is True:
            logs.print_notice("You have logged out of your account")
            show_prompt()
        else:
            logs.print_error("Couldn't log out")
            show_prompt()

    elif packet["type"] == TYPE_KICK:
        logs.print_notice(f"You have been logged out\n{packet['message']}")
        client.set_login(False)
        show_prompt()