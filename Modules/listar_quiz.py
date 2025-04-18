import sqlite3
import os
from discord.ext import commands
import discord

db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')

class listar_quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_id = 1100472796510957589  # ID do cargo necessário para usar o comando

    @commands.command(name="listar_quiz")
    async def listar_quiz(self, ctx):
        if discord.utils.get(ctx.author.roles, id=self.role_id) is None:
            await ctx.send("Você não tem permissão para usar este comando.")
            return

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT pergunta, resposta, categoria FROM quiz")
        quizzes = self.cursor.fetchall()
        self.conn.close()

        if not quizzes:
            await ctx.send("Nenhum quiz encontrado.")
            return

        for pergunta, resposta_quiz, categoria in quizzes:
            await ctx.send(f"""
            \r**Categoria:** {categoria}
            \r**Pergunta:** {pergunta}
            \r**Resposta:** {resposta_quiz}\n\n\r""")

async def setup(bot):
    await bot.add_cog(listar_quiz(bot))