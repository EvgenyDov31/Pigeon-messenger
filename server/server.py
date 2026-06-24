"""
Консольный месседжер

Pigeon server: 0.4.1
"""
VERSION = "0.4.1"

import socket
from threading import Thread
import sys
import json
from queue import Queue
from queue import Empty
import readline

from clients_list import ActiveClients
from message_parser import message_parser
import logs
from client import Client
from database.db_connector import DBConnector

IP_SERVER = socket.gethostbyname(socket.gethostname())
PORT_SERVER = 11000


class Server:
    """
    Объект сервера. Принимает IP сервера, его порт и .
    """
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip # IP сервера
        self.server_port = server_port # PORT сервера
        self.socket = None # Сокет сервера
        self.is_running = False # Запущен ли сервер
        self.accept_thread = None # Поток новых подключений
        self.buffer_parsing_thread = None # Поток парсинга сообщений
        
        self.db = DBConnector() 
        self.active_clients = ActiveClients()
        self.msg_buffer = Queue()


    def start_server(self, argv="-a") -> None:
        """
        Запускает сервер.
        """
        if argv in ("-h", "--help"):
            logs.print_start_server_help()
            return

        logs.create_log("Strarting server", log_type="info")

        if self.is_running:
            logs.print_notice("Server already running")
            return

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IPv4, TCP)

        # Разрешает повторно использовать порт
        self.socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

        try:
            self.socket.bind((self.server_ip, self.server_port))
            self.socket.settimeout(1)
            self.socket.listen(3)

            logs.print_notice(f"Start server. IP = {self.server_ip}, PORT = {self.server_port}")

            self.is_running = True

            self.create_buffer_parsing_thread()

            # Параметры запуска сервера:
            # Не принимать подключения
            if argv in ("-na", "--noaccept"):
                return

            # Запуск принятия подключений
            elif argv in ("-a", "--accept"):
                self.create_accepting_thread()

            else:
                logs.print_notice(f"Unknown argument \"{argv}\". Type \"start [--help / -h]\" to show arguments list")


        except OSError as err:
            if err.errno == 98:
                logs.print_error("Addres already in use", str(err))

        except Exception as err:
            logs.print_error("Couldn't start the server", str(err))


    def create_buffer_parsing_thread(self) -> None:
        """
        Создаёт поток парсинга буфера сообщений.
        """
        if self.socket is not None:
            if self.buffer_parsing_thread and self.buffer_parsing_thread.is_alive():
                logs.print_notice("Server already parsing buffer")
                return

            buffer_parsing_thread = Thread(
                target=self.start_buffer_parsing,
                daemon=True
            )
            buffer_parsing_thread.start()
            self.buffer_parsing_thread = buffer_parsing_thread
            logs.print_notice("Start message buffer parsing")
        
        else:
            logs.print_notice("Server is not running")


    def start_buffer_parsing(self) -> None:
        """
        Парсит буфер сообщений.
        """
        while self.is_running:
            try:
                data, client = self.msg_buffer.get(timeout=1)
            except Empty:
                continue

            try:
                packet = json.loads(data)

            except json.JSONDecodeError as err:
                logs.print_error(f"Invalid packet from {client.user_id}", str(err))
                continue
            
            except Exception as err:
                logs.print_error("Couldn't parsing buffer", str(err))

            message_parser(packet, client, self)


    def create_accepting_thread(self) -> None:
        """
        Создаёт поток подключений клиентов.
        """
        if self.socket is not None:
            if self.accept_thread and self.accept_thread.is_alive():
                logs.print_notice("Server already accepting")
                return

            accept_thread = Thread(
                target=self.start_accepting_connections,
                daemon=True
            )
            accept_thread.start() # Поток подключения новых клиентов
            self.accept_thread = accept_thread
            logs.print_notice("Start clients accepting")

        else:
            logs.print_notice("The server is not running")


    def start_accepting_connections(self) -> None:
        """
        Создаёт поток прослушки клиента.
        """
        while self.is_running:
            try:
                connection, user_ip = self.socket.accept()

                logs.print_notice(f"Client [{user_ip}] is connected")
                print("> ", end="", flush=True)

                client_session = Client(user_ip, connection)
                self.active_clients.add_client(connection, client_session)

                client_handler_thread = Thread(
                    target=self.handle_client,
                    args=(connection, ),
                    daemon=True
                )
                client_handler_thread.start() # Поток прослушки клиента
            
            except socket.timeout:
                continue

            except Exception as err:
                logs.print_error("User connection error", str(err))
                print("> ", end="", flush=True)


    def handle_client(self, connection: socket.socket) -> None:
        """
        Принимает данные от клиента.
        """
        try:
            buffer = ""
            client = self.active_clients.get_client_by_connection(connection)

            if client is None:
                return

            while self.is_running:
                try:
                    data = connection.recv(1024)

                    if not data:
                        logs.print_notice(f"Client {client.user_id} disconnected")
                        print("> ", end="", flush=True)
                        break

                    buffer += data.decode()

                    while "\n" in buffer:
                        message, buffer = buffer.split("\n", 1)

                        self.msg_buffer.put((message, client))


                except ConnectionResetError as err:
                    logs.print_error(f"Client {client.user_id} disconnected unexpectedly", str(err))
                    print("> ", end="", flush=True)
                    break

                except Exception as err:
                    logs.print_error("Couldn't get client data", str(err))

        finally:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except:
                pass

            connection.close()
            self.active_clients.remove_client(connection)


    def send_message_by_connection(self, data: dict, connection: socket.socket) -> None:
        """
        Отправляет сообщение клиенту по его подключению.
        Принимает сообщение и сокет клиента.
        """
        try:
            connection.sendall(data.encode())

        except Exception as err:
            logs.print_error(f"Couldn't send message", str(err))


    def send_message(self, data: str, to_user_id: int | str) -> bool:
        """
        Отправляет сообщение указанному клиенту.
        Принимает сообщение (json), ID получателя
        """
        client = self.active_clients.get_client_by_id(to_user_id)

        if client is None:
            logs.print_notice(f"User {to_user_id} not found")
            return False

        try:
            client.user_socket.sendall(data.encode())
            return True

        except Exception as err:
            logs.print_error(f"Couldn't send message", str(err))
            return False


    def stop_server(self) -> None:
        """
        Останавливает сервер.
        """
        logs.create_log("Stopping the server", log_type="info")
        
        if self.is_running == False:
            logs.print_notice("The server has not been started yet")
            return 

        # Закрываем подключения с клиентами
        for client in self.active_clients.active_clients.values():
            try:
                client.user_socket.shutdown(socket.SHUT_RDWR)
            except:
                pass

            client.user_socket.close()

        # Выключаем сервер
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

        self.accept_thread = None
        self.socket.close()
        self.is_running = False
        self.socket = None

        self.active_clients.remove_all()

        logs.print_notice("Server is stopped")
            

    def get_clients_list(self, argv="-c") -> None:
        """
        Возвращает список клинетов или сообщение с ошибкой.
        """
        if argv in ("-c", "--connected"):
            _clients_list = self.active_clients.get_clients_list()
            if _clients_list == []:
                logs.print_notice("There is no clients")

            for client in _clients_list:
                print(client)
            
            return
        
        elif argv in ("-h", "--help"):
            logs.print_clients_list_help_message()

        else:
            logs.print_notice(f"Unknown argument \"{argv}\". Type \"clients [--help / -h]\" to show arguments list")


def main() -> None:
    server = Server(IP_SERVER, PORT_SERVER)

    while True:
        command = input("\r> ")
        parts = command.split()

        if not parts:
            continue

        # Запуск сервера
        if parts[0] == "start":
            if len(parts) == 1:
                parts.append("-a")
            server.start_server(parts[1])
            
        # Остановка сервера
        elif command == "stop": 
            server.stop_server()

        # Вывод списка подключённых клиентов
        elif parts[0] == "clients":
            if len(parts) == 1:
                parts.append("-c")
            server.get_clients_list(parts[1])

        # Запустить принятие клиентов
        elif command == "staccept":
            server.create_accepting_thread()

        # Вывод списка команд
        elif command == "help":
            logs.print_server_help()

        # Завершение программы
        elif command == "exit":
            sys.exit()

        else:
            logs.print_notice("Unknown command. Type \"help\" to show commands list.")


if __name__ == "__main__":
    main()