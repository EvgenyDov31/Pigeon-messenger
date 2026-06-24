"""
Мессенджер

Модуль криптографии.
"""

import bcrypt

def hash_password(password: str) -> str:
    """
    Возвращает хешированный пароль.
    Принимает исходный пароль.
    """
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Возвращает True, если пароли совпадают.
    Принимает исходный и хешированный пароль.
    """
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )