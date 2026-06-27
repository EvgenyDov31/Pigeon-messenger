"""
Консольный месседжер

Модуль парсинга сообщений клиента
"""

import json
from message_types import TYPE_SEND, TYPE_LOGIN, TYPE_REGISTR, TYPE_DELETE_USER, TYPE_CHANGE_PASSWORD, TYPE_LOGOUT
from client import Client
from authorization import Authorization
import logs

def message_send(packet: dict, client: Client, server) -> None:
    """
    Формирует json и отправляет сообщение.
    """
    message = {
        "type": TYPE_SEND,
        "from": client.user_id, # ID отправителя (TODO: username)
        "message": packet["message"]
    }

    data = json.dumps(message) + "\n"
    to_user_id = packet["to"] # ID получателя

    server.send_message(data, to_user_id) # Отправка сообщения


def login_answer_send(result: bool, client: Client, server) -> None:
    """
    Отправляет клиенту статус авторизации.
    Принимает результат авторизации и объект клиента.
    """
    message = {
        "type": TYPE_LOGIN,
        "result": result
    }

    data = json.dumps(message) + "\n"

    server.send_message_by_connection(data, client.user_socket)


def registr_answer_send(result: bool, client: Client, server) -> None:
    """
    Отправляет клиенту статус регистрации.
    Принимает результат регистрации и объект клиента.
    """
    message = {
        "type": TYPE_REGISTR,
        "result": result
    }

    data = json.dumps(message) + "\n"

    server.send_message_by_connection(data, client.user_socket)


def logout_answer_send(result: bool, client: Client, server) -> None:
    """
    Отправляет клиенту статус выхода из аккаунта.
    Принимает результат выхода из аккаунта и объект клиента.
    """
    message = {
        "type": TYPE_LOGOUT,
        "result": result
    }

    data = json.dumps(message) + "\n"

    server.send_message_by_connection(data, client.user_socket)


def login_message(packet: dict, client: Client, server) -> None:
    """
    Парсит сообщение о логине.
    Принимает полученный пакет и объект клиента
    """
    user_id = packet.get("user_id")
    password = packet.get("password")
    auth = Authorization(client)

    if not user_id or not password:
        return

    if client.authenticated:
        return 

    result = auth.auth_user(password, user_id, server.db)
    if result:
        logs.print_notice(f"{user_id} is authotizated")

    login_answer_send(result, client, server) # Отправляем клиенту сообщение с результатом авторизации


def logaut_message(client: Client, server) -> None:
    """
    Парсит сообщение о выходе из аккаунта.
    Принимает объект клиента.
    """
    auth = Authorization(client)

    if client.authenticated:
        user_id = client.user_id
        auth.logout_user()
        logs.print_notice(f"User {user_id} is logged out")
        logout_answer_send(True, client, server)
        return

    logout_answer_send(False, client, server)

    
def registr_message(packet: dict, client: Client, server) -> None:
    """
    Парсит сообщение о регистрации.
    Принимает полученный пакет и объект клиента
    """
    user_id = packet.get("user_id")
    password = packet.get("password")
    username = packet.get("username")
    auth = Authorization(client)

    if len(user_id) > 30 or len(password) > 30 or len(username) > 50:
        registr_answer_send(result, client, server)
        return
 
    if not user_id or not password or not username:
        registr_answer_send(result, client, server)
        return

    result = auth.registration_user(user_id, password, username, server.db)

    if result:
        logs.print_notice(f"{user_id} registrated successful")
    
    registr_answer_send(result, client, server)


def delete_user_answer_send(result: bool, client: Client, server) -> None:
    """
    Отправляет клиенту статус удаления аккаунта.
    Принимает результат удаления и объект клиента.
    """
    message = {
        "type": TYPE_DELETE_USER,
        "result": result
    }

    data = json.dumps(message) + "\n"

    server.send_message_by_connection(data, client.user_socket)


def delete_user_message(client: Client, server) -> None:
    """
    Парсит сообщение о удалении аккаунта.
    Принимает полученный пакет и объект клиента.
    """
    auth = Authorization(client)

    result = auth.delete_user(client.user_id, server.db)

    if result:
        logs.print_notice(f"{client.user_id} deleted successful")

    delete_user_answer_send(result, client, server)


def change_user_password_answer(result: bool, client: Client, server) -> None:
    """
    Отправляет клиенту статус замены пароля аккаунта.
    Принимает результат замены пароля и объект клиента.
    """
    message = {
        "type": TYPE_CHANGE_PASSWORD,
        "result": result
    }

    data = json.dumps(message) + "\n"

    server.send_message_by_connection(data, client.user_socket)


def change_user_password(packet: dict, client: Client, server) -> None:
    """
    Парсит сообщение о замене пароля пользователя.
    Принимает полученный пакет и объект клиента.
    """
    auth = Authorization(client)

    result = auth.change_user_password(packet["new_password"], server.db)

    change_user_password_answer(result, client, server)


def message_parser(packet: dict, client: Client, server) -> None:
    """
    Парсит сообщение клиента.
    Принимает полученый пакет (сообщение), IP отправителя, объект сервера
    """
    if(packet["type"] == TYPE_SEND):
        if client.authenticated:
            message_send(packet, client, server)
            
    elif(packet["type"] == TYPE_LOGIN):
        login_message(packet, client, server)

    elif packet["type"] == TYPE_LOGOUT:
        logaut_message(client, server)

    elif packet["type"] == TYPE_REGISTR:
        registr_message(packet, client, server)

    elif packet["type"] == TYPE_DELETE_USER:
        if client.authenticated:
            delete_user_message(client, server)
    
    elif packet["type"] == TYPE_CHANGE_PASSWORD:
        if client.authenticated:
            change_user_password(packet, client, server)
            
            