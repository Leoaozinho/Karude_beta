def criar_tabela(self):
    self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mod_id INTEGER NOT NULL,
            motivo TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    self.conexao.commit()
