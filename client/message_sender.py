"""
Консольный месседжер

Модуль компановки и отправки сообщений на сервер
"""

import socket
import json
from message_types import TYPE_SEND, TYPE_LOGIN, TYPE_REGISTR, TYPE_DELETE_USER, TYPE_CHANGE_PASSWORD, TYPE_LOGOUT
import logs


def send_packet(socket, packet) -> None:
    """
    Отправляет составленный пакет.
    Принимает сокет клиента и пакет.
    """
    data = json.dumps(packet) + "\n"
    try:
        socket.sendall(data.encode())
        logs.print_notice(f"processing...")
    
    except:
        logs.print_error("Couldn't send packet")


def registr_message(client_socket: socket.socket, user_id: str, username: str, password: str) -> None:
    """
    Передаёт сообщение о регистрации на сервер. 
    Принимает сокет, ID, пароль и имя пользователя.
    """
    request = {
        "type": TYPE_REGISTR,
        "user_id": user_id,
        "password": password, 
        "username": username
    }

    send_packet(client_socket, request)


def delete_accaunt_message(client_socket: socket.socket) -> None:
    """
    Передаёт сообщение о удалении аккаунта на сервер. 
    Принимает сокет пользователя.
    """
    request = {
        "type": TYPE_DELETE_USER
    }

    send_packet(client_socket, request)


def change_password_message(client_socket: socket.socket, new_password: str) -> None:
    """
    Передаёт сообщение о смене пароля на сервер. 
    Принимает сокет пользователя.
    """
    request = {
        "type": TYPE_CHANGE_PASSWORD, 
        "new_password": new_password
    }

    send_packet(client_socket, request)


def logout_message(client_socket: socket.socket) -> None:
    """
    Передаёт сообщение о выходе из аккаунта на сервер. 
    Принимает сокет пользователя.
    """
    request = {
        "type": TYPE_LOGOUT
    }

    send_packet(client_socket, request)


def login_message(client_socket: socket.socket, password: str, user_id: str) -> None:
    """
    Передаёт сообщение о входе на сервер. 
    Принимает сокет, пароль и имя пользователя.
    """
    request = {
        "type": TYPE_LOGIN,
        "user_id": user_id,
        "password": password
    }

    send_packet(client_socket, request)


def message_to_user(client_socket: socket.socket, user_id: str, message: str) -> None:
    """
    Передаёт сообщение на сервер для отправки его клиенту
    """
    request = {
        "type": TYPE_SEND,
        "to": user_id,
        "message": message
    }

    send_packet(client_socket, request)
        
