"""
Консольный месседжер.
Модуль хранения пользователей
"""

import socket
from client import Client

class ActiveClients:
    """
    Хранит IP и socket подключённых пользователей.
    """
    def __init__(self):
        self.active_clients: dict[socket.socket, Client] = {}


    def add_client(self, connection: socket.socket, client_session: Client) -> None:
        """
        Добавление клиента в список подключённых клиентов.
        """
        self.active_clients[connection] = client_session

    
    def remove_client(self, connection: socket.socket) -> None:
        """
        Удаление клиента из списка подключённых клиентов.
        """
        self.active_clients.pop(connection, None)

    
    def get_client_by_connection(self, connection: socket.socket) -> Client:
        """
        Возвращает сокет клиента по его IP.
        """
        return self.active_clients.get(connection)


    def get_client_by_id(self, id: str) -> Client | None:
        """
        Возвращает объект клиента по его id.
        """
        for client in self.active_clients.values():
            if client.user_id == id:
                return client
        return None


    def get_clients_list(self) -> list:
        """
        Возвращает список подключённых клиентов
        """
        return [f"{value.user_ip} -> {value.user_id}" for key, value in self.active_clients.items()]

    
    def get_socket_by_user_id(self, user_id: str) -> socket.socket | None:

        for client in self.active_clients.values():
            if client.user_id == user_id:
                return client.user_socket

        return None


    def remove_all(self) -> None:
        """
        Очищает список.
        """
        self.active_clients.clear()
    