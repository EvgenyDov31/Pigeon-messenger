"""
Мессенджер

Модуль управления БД.
"""


from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import logs
from database.db_models import User, Base
from database.db_url import DB_URL


class DBConnector:

    def __init__(self):
        self.engine = create_engine(DB_URL)   
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.User = User
        Base.metadata.create_all(bind=self.engine)


    def add_new_user(self, user_id: str, username: str, password_hash: str) -> bool:
        """
        Добавление нового пользователя в БД. 
        Принимает его username и password.
        """
        try:
            db = self.SessionLocal()

            new_user = self.User(user_id=user_id, username=username, password_hash=password_hash)

            db.add(new_user)
            db.commit()
            # self.cursor.execute(
            #     "INSERT INTO users (user_id, username, password_hash) VALUES (?, ?, ?)",
            #     (user_id, username, password_hash)
            # )
            # self.db.commit()
            return True

        except Exception as err:
            db.rollback()
            logs.print_error("Couldn't add new user to database", str(err))
            return False

        finally:
            db.close()


    def replace_user_password(self, user_id: str, new_password: str) -> bool:
        """
        Заменяет пароль на новый в БД. 
        Принимает user_id и новый пароль пользователя.
        """
        try:
            db = self.SessionLocal()
            result = db.query(self.User).filter(self.User.user_id == user_id).update(
                {self.User.password_hash: new_password},
                synchronize_session="evaluate" 
            )
            db.commit()

            return result > 0

        except Exception as err:
            db.rollback()
            logs.print_error("Couldn't change password in database", str(err))
            return False

        finally:
            db.close()


    def auth_user(self, user_id: str) -> str | None:
        """
        Авторизация пользователя.
        Возвращает username.
        Принимает его id и пароль.
        """
        try:
            db = self.SessionLocal()

            result = db.query(self.User.username).filter(self.User.user_id == user_id).first()

            if result:
                return result[0]

            return None

        except Exception as err:
            logs.print_error("Couldn't select user in database", str(err))
            return None

        finally:
            db.close()


    def get_user_password(self, user_id: str) -> str | None:
            """
            Получение пароля пользователя.
            Возвращает password_hash по id.
            Принимает id пользователя.
            """
            try:
                db = self.SessionLocal()

                result = db.query(self.User.password_hash).filter(self.User.user_id == user_id).first()

                if result:
                    return result[0]

                return None

            except Exception as err:
                logs.print_error("Couldn't select user password in database", str(err))
                return None

            finally:
                db.close()


    def user_id_exists(self, user_id: str) -> bool:
        """
        Возвращает True, если пользователь с данным ID существует.
        """
        try:
            db = self.SessionLocal()
            result = db.query(1).filter(self.User.user_id == user_id).first()
            return result is not None

        except Exception as err:
            logs.print_error("Couldn't select user in database", str(err))
            return False

        finally:
            db.close()


    def user_exists(self, username: str) -> bool:
        """
        Возвращает True если такой пользователь существует.
        Принимает имя пользователя.
        """
        try:
            db = self.SessionLocal()
            result = db.query(1).filter(self.User.username == username).first()
            return result is not None
        
        except Exception as err:
            logs.print_error("Couldn't select username in database", str(err))
            return False

        finally:
            db.close()


    def delete_user(self, user_id: str) -> bool:
        """
        Удаляет запись клиента из БД.
        Принимает ID пользователя.
        """
        try:
            db = self.SessionLocal()
            result = db.query(self.User).filter(self.User.user_id == user_id).delete()
            db.commit()

            return result > 0
        
        except Exception as err:
            db.rollback()
            logs.print_error("Couldn't delete user from DB", str(err))
            return False

        finally:
            db.close()
