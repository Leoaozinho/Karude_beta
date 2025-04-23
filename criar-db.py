import os
import sqlite3

# Caminho absoluto para o arquivo do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'users', 'users.db')

# Conexão com o banco de dados
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Criação da tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER NOT NULL UNIQUE,
        userXp INTEGER NOT NULL DEFAULT 0,
        userWallet INTEGER NOT NULL DEFAULT 0,
        userLevel INTEGER NOT NULL DEFAULT 1,
        lastMsg DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print('✅ Tabela "usuarios" criada com sucesso.')

    # Criação da tabela de itens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        valor REAL NOT NULL
    );
    """)
    print('✅ Tabela "itens" criada com sucesso.')

    # Criação da tabela de compras
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES usuarios(id),
        FOREIGN KEY(item_id) REFERENCES itens(id)
    );
    """)
    print('✅ Tabela "compras" criada com sucesso.')

    # Criação da tabela de quiz
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        categoria TEXT NOT NULL
    );
    """)
    print('✅ Tabela "quiz" criada com sucesso.')

    # Criação da tabela de avisos (warnings)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mod_id INTEGER NOT NULL,
        motivo TEXT NOT NULL,
        data TEXT NOT NULL
    );
    """)
    print('✅ Tabela "warnings" criada com sucesso.')

    # Criação da tabela de perguntas de trivia
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trivia_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    );
    """)
    print('✅ Tabela "trivia_questions" criada com sucesso.')

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS welcome_config (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
    """)
    print('✅ Tabela "welcome_config" criada com sucesso.')

    conn.commit()