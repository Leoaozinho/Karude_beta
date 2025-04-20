# Modules/Database/db_connection.py
import sqlite3
import os

class DatabaseConnection:
    def __init__(self, db_filename="user.db"):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.db_path = os.path.join(base_dir, 'Database', db_filename)
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")  # ativa verificação de chaves estrangeiras
        except sqlite3.Error as e:
            print(f"[Erro na conexão com SQLite]: {e}")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.commit()
        except sqlite3.Error as e:
            print(f"[Erro ao executar query]: {e}")

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()