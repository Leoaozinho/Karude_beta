import os
import sqlite3

# wibly
db_path = os.path.join(os.path.dirname(__file__), 'users', 'users.db')

# wobly
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# pegando os nomes das tabelas do banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()

# lendo os dados de cada tabela
for (tabela,) in tabelas:
    print(f"\n🔸 Tabela: {tabela}")
    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        registros = cursor.fetchall()

        if registros:
            for registro in registros:
                print(registro)
        else:
            print("   (Sem registros)")
    except Exception as e:
        print(f"   ⚠️ Erro ao acessar tabela {tabela}: {e}")

#  com cloze
conn.close()