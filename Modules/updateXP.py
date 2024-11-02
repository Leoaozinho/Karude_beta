from discord import Message
from discord.ext import commands
from datetime import datetime, timedelta
import sqlite3
import os

# verificar se já tem conta.
# se não tiver, é criada.
def add_user(user_id):
    db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()
        
        # Verificando se o usuário já existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE userId = ?", (user_id,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            return "usuário já cadastrado"
        else:
            atual_datetime = datetime.now()
            data_ajustada = atual_datetime - timedelta(hours=24)
            data_ajustada_formatada = data_ajustada.strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
            INSERT INTO usuarios (userId, userXp, userWallet, userLevel, lastMsg)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, 0, 0, 1, data_ajustada_formatada))

            conn.commit()

            return "usuario criado com sucesso"

    except sqlite3.Error as e:
        print(f'Erro ao adicionar usuário: {e}')

    finally:
        # Fechando a conexão
        conn.close()

# add xp a cada msg
def add_xp(user_id, xp_to_add):
    db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')
    conn = sqlite3.connect(db_path)
    
    try:
        cursor = conn.cursor()
        # Iniciando uma transação
        cursor.execute("BEGIN")

        cursor.execute("SELECT userXp, userLevel FROM usuarios WHERE userId = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            current_xp, current_level = result
            new_xp = current_xp + xp_to_add

            if new_xp < 1000:
                new_level = 1
            else:
                new_level = new_xp // 1000 # dividindo por 1000

            # Atualizando o XP e o nível do usuário no DB
            cursor.execute("""
            UPDATE usuarios
            SET userXp = ?, userLevel = ?
            WHERE userId = ?
            """, (new_xp, new_level, user_id))
            
            # Salvando (commit) as alterações da transação
            conn.commit()
            return
        else:
            print('Usuário não encontrado.')
    
    except sqlite3.Error as e:
        print(f'Erro ao atualizar XP do usuário: {e}')
        conn.rollback()  # Desfazendo alterações em caso de erro
    
    finally:
        # Fechando a conexão
        conn.close()

class updateXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # Ignorar mensagens do próprio bot
        if message.author == self.bot.user:
            return
        add_user(int(message.author.id))
        add_xp(message.author.id, 20)

async def setup(bot: commands.Bot):
    await bot.add_cog(updateXP(bot))