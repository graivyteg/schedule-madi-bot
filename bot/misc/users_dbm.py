from databases.database_manager import DatabaseManager
from databases.models.user import User


class UsersDBM(DatabaseManager):
    def __init__(self, database_name):
        super().__init__(database_name)
        self.init_table()

    def init_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT,
            study_group TEXT
        );'''
        self.cur.execute(sql)
        self.conn.commit()

    def add_user(self, user: User):
        sql = f'''INSERT INTO users (id, name, study_group) VALUES (
            {user.id}, '{user.name}', '{user.group}');'''
        self.cur.execute(sql)
        self.conn.commit()

    def try_get_user(self, user_id):
        sql = f'''SELECT * FROM users WHERE id={user_id};'''
        self.cur.execute(sql)
        user = self.cur.fetchone()
        print(f'User find result: {user}')
        if user is None:
            return False
        else:
            return User(
                id=user[0],
                name=user[1],
                group=user[2]
            )

    def get_or_add_user(self, user_id) -> User:
        user = self.try_get_user(user_id)
        if not user:
            user = User(id=user_id, name='', group='')
            self.add_user(user)
        return user

    def update_user(self, user: User):
        sql = f'''UPDATE users SET name='{user.name}', study_group='{user.group}' WHERE id={user.id}'''
        self.cur.execute(sql)
        self.conn.commit()