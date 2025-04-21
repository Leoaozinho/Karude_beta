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

    def trivia_questions(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trivia_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        self.conexao.commit()
