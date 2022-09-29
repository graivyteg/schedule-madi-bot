import os
import sqlite3

class DatabaseManager:
    def __init__(self, database_name):
        path = f'databases/list/{database_name}.sqlite3'
        if not os.path.exists(path):
            open(path, 'w+')
        self.conn = sqlite3.connect(f'databases/list/{database_name}.sqlite3')
        self.cur = self.conn.cursor()




