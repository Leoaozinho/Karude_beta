import discord
from discord.ext import commands
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')

def inserir_quiz(pergunta: str, resposta: str, categoria: str) -> str:
    if not pergunta or not resposta or not categoria:
        return "Todos os parâmetros (pergunta, resposta e categoria) são obrigatórios."
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO quiz (pergunta, resposta, categoria) VALUES (?, ?, ?)", (pergunta, resposta, categoria))
        conn.commit()
        conn.close()
        return f"Pergunta adicionada com sucesso!\n\n\rPergunta: {pergunta}\nResposta: {resposta}\nCategoria: {categoria}"
    
    except Exception as e:
        return f"Ocorreu um erro ao inserir os dados: {e}"

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="adicionar_quiz")
    async def adicionar_quiz(self, ctx, pergunta: str = None, resposta: str = None, categoria: str = None):
        role_id = 1263827423569645710
        if discord.utils.get(ctx.author.roles, id=role_id) is None:
            await ctx.send("Você não tem permissão para usar este comando.")
            return

        resultado = inserir_quiz(pergunta, resposta, categoria)
        await ctx.send(resultado)

async def setup(bot):
    await bot.add_cog(QuizCog(bot))