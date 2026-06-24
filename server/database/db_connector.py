"""
Мессенджер

Модуль управления БД.
"""

import sqlite3
import logs

class DBConnector:

    def __init__(self):
        self.db = sqlite3.connect("database/users.db", check_same_thread=False)
        self.cursor = self.db.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)

        self.db.commit()


    def add_new_user(self, user_id: str, username: str, password_hash: str) -> bool:
        """
        Добавление нового пользователя в БД. 
        Принимает его username и password.
        """
        try:
            self.cursor.execute(
                "INSERT INTO users (user_id, username, password_hash) VALUES (?, ?, ?)",
                (user_id, username, password_hash)
            )
            self.db.commit()
            return True

        except Exception as err:
            logs.print_error("Couldn't add new user to database", str(err))
            return False


    def replace_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Заменяет пароль на новый в БД. 
        Принимает user_id и новый пароль пользователя.
        """
        try:
            self.cursor.execute(
                "UPDATE users SET password_hash = ? WHERE user_id = ?",
                (new_password, user_id)
            )
            self.db.commit()
            return True

        except Exception as err:
            logs.print_error("Couldn't change password in database", str(err))
            return False


    def auth_user(self, user_id: str) -> str | None:
        """
        Авторизация пользователя.
        Возвращает username.
        Принимает его id и пароль.
        """

        try:
            self.cursor.execute(
                "SELECT username FROM users WHERE user_id = ?",
                (user_id, )
            )

            result = self.cursor.fetchone()

            if result:
                return result[0]

            return None

        except Exception as err:
            logs.print_error("Couldn't select user in database", str(err))


    def get_user_password(self, user_id: str) -> str | None:
            """
            Получение пароля пользователя.
            Возвращает password_hash по id.
            Принимает id пользователя.
            """
            try:
                self.cursor.execute(
                    "SELECT password_hash FROM users WHERE user_id = ?",
                    (user_id, )
                )

                result = self.cursor.fetchone()

                if result:
                    return result[0]

                return None

            except Exception as err:
                logs.print_error("Couldn't select user password in database", str(err))


    def user_id_exists(self, user_id: str) -> bool:
        self.cursor.execute(
            "SELECT 1 FROM users WHERE user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchone() is not None


    def user_exists(self, username: str) -> bool:
        """
        Возвращает True если такой пользователь существует.
        Принимает имя пользователя.
        """
        self.cursor.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )

        return self.cursor.fetchone() is not None


    def delete_user(self, user_id: str) -> bool:
        """
        Удаляет запись клиента из БД.
        Принимает ID пользователя.
        """
        try:
            self.cursor.execute(
                "DELETE FROM users WHERE user_id = ?",
                (user_id, )
            )

            self.db.commit()

            return self.cursor.rowcount > 0
        
        except Exception as err:
            logs.print_error("Couldn't delete user from DB", str(err))
            return False


    def close(self):
        """
        Закрывает подключение к БД.
        """
        self.db.close()