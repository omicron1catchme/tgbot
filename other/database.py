import sqlite3


class Database:

    def __init__(self, path_db_file):
        self.connection = sqlite3.connect(database=path_db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS users(
	"user_id"	INTEGER NOT NULL DEFAULT '-',
	"login"	TEXT NOT NULL DEFAULT '-',
	"password"	TEXT NOT NULL DEFAULT '-',
	"access_token"	TEXT NOT NULL DEFAULT '-',
	PRIMARY KEY("user_id")
)""")

    #  *****************************  ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ В БД  *****************************

    def add_user(self, user_id) -> None:
        # добавить нового пользователя в БД
        with self.connection:
            self.cursor.execute(f'INSERT INTO users (user_id) VALUES ({user_id})')

    #  *****************************  ДОБАВИТЬ ЛОГИН ПАРОЛЬ ТОКЕН В БД  *****************************
    def set_login(self, user_id, login) -> None:
        # обновить логин пользователя в БД
        with self.connection:
            self.cursor.execute(f"""UPDATE users
                                    SET login = '{login}'
                                    WHERE user_id == {user_id}""")

    def set_password(self, user_id, password) -> None:
        # обновить пароль пользователя в БД
        with self.connection:
            self.cursor.execute(f"""UPDATE users 
                                    SET password = '{password}'
                                    WHERE user_id == {user_id}""")

    def set_token(self, user_id, access_token) -> None:
        # добавить токен пользователя
        with self.connection:
            self.cursor.execute(f"""UPDATE users 
                                    SET access_token = '{access_token}'
                                    WHERE user_id == {user_id}""")

    #  *****************************  ПОЛУЧИТЬ ЗНАЧЕНИЯ ЯЧЕЕК ИЗ БД  *****************************

    def exists_user(self, user_id) -> bool:
        # проверить есть ли такой пользователь в БД
        with self.connection:
            response = self.cursor.execute(f"""SELECT user_id
                                               FROM users 
                                               WHERE user_id == {user_id} """).fetchone()
            return bool(response)

    def get_user_inf(self, user_id) -> dict:
        # ПОЛУЧИТЬ ЛОГИН ИЛИ ПАРОЛЬ ИЛИ ТОКЕН ПОЛЬЗОВАТЕЛЯ
        with self.connection:
            inf = zip(('login', 'password', 'token'),
                      self.cursor.execute(f"""SELECT login, password, access_token
                                              FROM users
                                              WHERE user_id == {user_id}""").fetchone())
        return dict(inf)

