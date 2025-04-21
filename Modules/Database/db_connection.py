# Modules/Database/db_connection.py
import sqlite3
import os

class DatabaseConnection:
    def __init__(self, db_filename="user.db"):
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Sobe uma pasta
        db_dir = os.path.join(base_dir, "Database")
        os.makedirs(db_dir, exist_ok=True)

        self.db_path = os.path.join(db_dir, db_filename)
        self.conn = None
        self.cursor = None

        self.connect()
        self.create_user_table_if_not_exists()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            print("[DB] Conexão com o banco de dados estabelecida com sucesso.")
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao conectar com SQLite: {e}")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            print("[DB] Conexão com banco de dados encerrada.")

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] ao executar query: {query} | Erro: {e}")

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

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
        try:
            self.cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO users (user_id, xp, nivel, saldo) VALUES (?, 0, 1, 0)",
                    (user_id,)
                )
                self.conn.commit()
                print(f"[DB] Novo usuário adicionado ao banco: {user_id}")
        except Exception as e:
            print(f"[ERRO] Falha ao garantir existência do usuário {user_id}: {e}")

    def get_user_info(self, user_id):
        try:
            self.cursor.execute("SELECT xp, nivel, saldo FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[ERRO] Falha ao buscar dados do usuário {user_id}: {e}")
            return None