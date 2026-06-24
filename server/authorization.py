"""
Мессенджер

Модуль авторизации клиента.
"""

from client import Client
from database.db_connector import DBConnector
import logs
import secure


class Authorization:

    def __init__(self, client_session: Client):
        """
        Класс авторизации клиента. 
        Принимает объект клиента.
        """
        self.client_session = client_session

    
    def auth_user(self, password: str, user_id: str, db_connector: DBConnector) -> bool:
        """
        Авторизация пользователя.
        Возвращает True если авторизация успешна
        Принимает пароль и user_id.
        """
        password_hash = db_connector.get_user_password(user_id)

        if password_hash:
            try:
                if secure.verify_password(password, password_hash):
                    username = db_connector.auth_user(user_id)

                    if username is None:
                        return False

                    self.client_session.login(user_id, username)
                    
                    return True
            
            except Exception as err:
                logs.print_error("Couldn't verify password hash", str(err))
                return False

        return False


    def logout_user(self) -> None:
        """
        Выход из аккаунта.
        """
        self.client_session.logout()


    def registration_user(self, user_id: str, password: str, username: str, db_connector: DBConnector) -> bool:
        """
        Регистрация пользователя.
        Возвращает True если регистрация успешна.
        Принимает имя пользователя и пароль.
        """
        if db_connector.user_id_exists(user_id):
            # logs.print_error("User ID already exists")
            return False

        password_hash = secure.hash_password(password)

        return db_connector.add_new_user(user_id, username, password_hash)


    def change_user_password(self, new_password: str, db_connector: DBConnector) -> bool:
        """
        Замена пароля пользователя.
        Возвращает True если замена пароля успешна.
        Принимает новый пароль.
        """
        password_hash = secure.hash_password(new_password)
        return db_connector.replace_user_password(self.client_session.user_id, password_hash)


    def delete_user(self, user_id: str, db_connector: DBConnector) -> bool:
        """
        Удаление аккаунта пользователя.
        Принимает ID пользователя.
        """
        return db_connector.delete_user(user_id)