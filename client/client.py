"""
Консольный месседжер

Pigeon client: 0.3.5
"""
VERSION = "0.3.5"

import socket
from threading import Thread
import sys
import json
import readline
from queue import Queue
from queue import Empty

import message_sender
from message_parser import message_parser
import logs

IP_SERVER = "127.0.1.1"
PORT_SERVER = 11000

class Client:
    """
    Объект клиента. Принимает IP сервера и его порт.
    """
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.is_connected = False
        self.recv_thread = None
        self.buffer_parsing_thread = None # Поток парсинга сообщений
        self.is_login = False
        self.msg_buffer = Queue()
        
    
    def connect_to_server(self) -> None:
        """
        Подключение к серверу.
        """
        if self.is_connected:
            logs.print_notice("You are already connected")
            return
        
        else:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)
                self.socket.connect((self.server_ip, self.server_port))
                self.is_connected = True

                self.create_buffer_parsing_thread()

                logs.print_notice(f"Connection successfully\nServer: \nIP: {self.server_ip} \nPORT: {self.server_port}")
            
            except:
                logs.print_error("Failed to connect to server")


    def create_buffer_parsing_thread(self) -> None:
        """
        Создаёт поток парсинга буфера сообщений.
        """
        if self.socket is not None and self.is_connected:
            if self.buffer_parsing_thread and self.buffer_parsing_thread.is_alive():
                logs.print_notice("Client already parsing buffer")
                return

            buffer_parsing_thread = Thread(
                target=self.start_buffer_parsing,
                daemon=True
            )
            buffer_parsing_thread.start()
            self.buffer_parsing_thread = buffer_parsing_thread
            logs.print_notice("Start message buffer parsing")
        
        else:
            logs.print_notice("Client is not connected with server")


    def start_buffer_parsing(self) -> None:
        """
        Парсит буфер сообщений.
        """
        while self.is_connected:
            try:
                data = self.msg_buffer.get(timeout=1)
            except Empty:
                continue

            try:
                packet = json.loads(data)

            except json.JSONDecodeError as err:
                logs.print_error(f"Invalid packet")
                continue
            
            except Exception as err:
                logs.print_error("Couldn't parsing buffer")

            message_parser(packet, self)

    
    def start_server_recv(self) -> None:
        """
        Создаёт поток прослушки сервера. 
        """
        if self.recv_thread == None and self.is_connected:
            self.recv_thread = Thread(
                target=self.server_recv_loop,
                daemon=True
            )
            self.recv_thread.start()


    def server_recv_loop(self) -> None:
        """
        Прослушивание сообщений с сервера.
        """
        try:
            buffer = ""
            while self.is_connected:
                try:
                    data = self.socket.recv(1024)

                    if not data:
                        logs.print_notice("Lose connection with server")
                        print("> ", end="", flush=True)
                        self.close_connection()
                        break

                    buffer += data.decode()

                    while "\n" in buffer:
                        message, buffer = buffer.split("\n", 1)

                        self.msg_buffer.put(message)


                except ConnectionResetError:
                    logs.print_error("Lose connection with server unexpectedly")
                    print("> ", end="", flush=True)
                    break
        
        finally:
            self.close_connection()


    def close_connection(self) -> None:
        """
        Закрывает подключение к серверу.
        """
        if self.is_connected == False:
            logs.print_notice("You are already disconnected")
            return

         # Выключаем сокет клиента
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

        self.socket.close()
        self.socket = None
        self.is_connected = False
        self.recv_thread = None
        self.is_login = False

        logs.print_notice("Disconnected")
        print("> ", end="", flush=True)


    def send_message(self, user_id: str, message: str) -> None:
        """
        Отправляет сообщение указанному клиенту.
        """
        if len(message) > 300:
            logs.print_notice("The maximum number of characters in a message is 300")
            return

        if self.is_connected and self.is_login:
            try:
                message_sender.message_to_user(self.socket, user_id, message)

            except Exception as ex:
                logs.print_error(f"Input error.\n{str(ex)}")

        elif not self.is_connected:
            logs.print_error("There is no connection to the server")

        elif not self.is_login:
            logs.print_error("You are not logged in")


    def login_message(self, user_id: str, password: str) -> None: #(TODO)
        """
        Отправляет сообщение в данными для входа.
        Принимает ID пользователя и его пароль.
        """
        if len(password) > 30:
            logs.print_notice("The maximum password length is 30")
            return

        if len(user_id) > 30:
            logs.print_notice("The maximum user id length is 30")
            return
            
        if self.is_connected:
            try:
                message_sender.login_message(self.socket, password, user_id)

            except Exception as err:
                logs.print_error("Couldn't send login data")

        else:
            logs.print_notice("There is no connection to the server")


    def logout_message(self) -> None:
        """
        Отправляет сообщение о выходе из аккаунта.
        """
        if self.is_connected and self.is_login:
            try:
                message_sender.logout_message(self.socket)

            except Exception as err:
                logs.print_error("Couldn't send login message to server")

        elif not self.is_connected:
            logs.print_notice("There is no connection to the server")

        elif not self.is_login:
            logs.print_notice("You are not logined")            


    def registr_message(self, user_id: str, username: str, password: str) -> None:
        """
        Отправляет сообщение c данными для регистрации.
        Принимает ID пользователя, имя и его пароль.
        """
        if len(password) > 30:
            logs.print_notice("The maximum password length is 30")
            return

        if len(user_id) > 30:
            logs.print_notice("The maximum user id length is 30")
            return

        if len(username) > 50:
            logs.print_notice("The maximum username length is 50")
            return

        if self.is_connected:
            try:
                message_sender.registr_message(self.socket, user_id, username, password)

            except Exception as err:
                logs.print_error("Couldn't send registration data")

        else:
            logs.print_error("There is no connection to the server")

    
    def change_password_message(self, new_password: str) -> None:
        """
        Отправляет сообщение с новым паролем для миены пароля.
        Принимает новый пароль пароль.
        """
        if len(password) > 30:
            logs.print_notice("The maximum password length is 30")
            return
            
        if self.is_connected and self.is_login:
            try:
                message_sender.change_password_message(self.socket, new_password)

            except Exception as err:
                logs.print_error("Couldn't send registration data")

        elif not self.is_connected:
            logs.print_notice("There is no connection to the server")
        
        elif not self.is_login:
            logs.print_notice("You are not logined")


    def delete_accaunt_message(self) -> None:
        """
        Отправляет сообщение об удалении аккаунта.
        """
        if self.is_connected:
            try:
                message_sender.delete_accaunt_message(self.socket)

            except Exception as err:
                logs.print_error("Couldn't send request to the server")

        else:
            logs.print_error("There is no connection with server")


    def is_server_recv(self) -> tuple:
        """
        Возвращает True, если поток прослушки сервера существует и True если он работает.
        """
        return (
            self.recv_thread is not None
            and self.recv_thread.is_alive()
        )


    def is_user_login(self) -> bool:
        """
        Возвращает True, если пользователь авторизован.
        """
        return self.is_login


    def is_server_connected(self) -> bool:
        """
        Возвращает True, если есть подключение с сервером.
        """
        return self.is_connected


    def set_login(self, is_login: bool) -> None:
        """
        Устанавливает статус авторизации.
        Принимает True или False.
        """
        self.is_login = is_login


    def print_message(self, from_user_ip: str, message: str) -> None:
        """
        Выводит сообщение.
        Принимает IP отправителя и текст сообщения.
        """
        print(f"\r[{from_user_ip}]: {message}")
        print("> ", end="", flush=True)


def registration(client: Client) -> None:
    """
    Получение данных для регистрации от пользователя.
    """
    print("Registration:")
    user_id = input("user id: ")
    username = input("username: ")
    password = input("password: ")

    if user_id and username and password:
        client.registr_message(user_id, username, password)
    else:
        logs.print_notice("Wrong input data")


def delete_accaunt(client: Client) -> None:
    """
    Удаление аккаунта пользователя.
    Принимает объект клиента.
    """
    result = input("Delete accaunt? [y/n]: ").lower()

    if result == "y":
        client.delete_accaunt_message()
    else:
        return


def change_password(client: Client) -> None:
    """
    Смена пароля пользователя.
    Принимает объект клиента.
    """
    new_password = input("Leave the line blank and press enter to cancel\nEnter new password: ")

    if new_password:
        client.change_password_message(new_password)



def main() -> None:
    # IP_SERVER = input("Server IP: ")
    client = Client(IP_SERVER, PORT_SERVER)

    while True:
        command = input("\n> ")
        parts = command.split()

        if not parts:
            continue
        # Подключение к серверу
        elif command == "connect":
            client.connect_to_server()
            client.start_server_recv()               

        # Разъединение подключения с сервером
        elif command == "disconnect":
            client.close_connection()
            
        # Отправка сообщения клиенту    
        elif parts[0] == "send":
            if len(parts) < 3:
                logs.print_client_help()
                
            if len(parts) >= 3:
                user_id = parts[1]
                message_list = parts[2:]
                message = " ".join(message_list)
                client.send_message(user_id, message)

        # Авторизация   
        elif parts[0] == "login":
            if len(parts) < 3:
                logs.print_client_help()

            if len(parts) >= 3:
                user_id = parts[1]
                password_list = parts[2:]
                password = " ".join(password_list)
                client.login_message(user_id, password)

        # Выход из аккаунта
        elif command == "logout":
            client.logout_message()

        # Регистрация
        elif command == "registration":
            registration(client)

        # Удаление аккаунта
        elif command == "deleteAccaunt":
            delete_accaunt(client)

        # Смена пароля
        elif command == "changePassword":
            change_password(client)

        # Вывод статуса авторизации 
        elif command == "loginStatus":
            client.is_user_login()

        # Вывод всех команд
        elif command == "help":
            logs.print_client_help()
        
        # Завершение программы
        elif command == "exit":
            sys.exit()

        else:
            print("Unknown command. Type \"help\" to show commands list.")

if __name__ == "__main__":
    main()