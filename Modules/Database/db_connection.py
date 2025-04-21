# Modules/Database/db_connection.py
import sqlite3
import os

import os
import sqlite3

class DatabaseConnection:
    def __init__(self, db_filename="user.db"):
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Sobe uma pasta
        db_dir = os.path.join(base_dir, "Database")
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, db_filename)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.connect()
        self.create_user_table_if_not_exists()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
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

    # --- NOVAS FUNÇÕES PARA INTEGRAÇÃO COM O COG DO USUÁRIO ---

    def create_user_table_if_not_exists(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1,
                saldo INTEGER DEFAULT 0
            )
        """)

    def ensure_user_exists(self, user_id):
        self.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not self.fetchone():
            self.execute("INSERT INTO users (user_id, xp, nivel, saldo) VALUES (?, 0, 1, 0)", (user_id,))

    def get_user_info(self, user_id):
        self.execute("SELECT xp, nivel, saldo FROM users WHERE user_id = ?", (user_id,))
        result = self.fetchone()
        if result:
            xp, nivel, saldo = result
            return {
                "xp": xp,
                "nivel": nivel,
                "saldo": saldo
            }
        else:
            return {
                "xp": 0,
                "nivel": 1,
                "saldo": 0
            }