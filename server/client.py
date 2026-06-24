"""
Мессенджер

Класс клиента.
"""

import socket

class Client:

    def __init__(self, user_ip: str, user_socket: socket.socket):
        self.user_ip = user_ip
        self.user_socket = user_socket
        self.username = None
        self.user_id = None
        self.authenticated = False


    def login(self, user_id: str, username: str) -> None:
        """
        Авторизация клиента.
        """
        self.user_id = user_id
        self.username = username
        self.authenticated = True
        

    def logout(self) -> None:
        """
        Выход из аккаунта.
        """
        self.username = None
        self.user_id = None
        self.authenticated = False