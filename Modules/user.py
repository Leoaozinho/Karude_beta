import os
import sqlite3
import discord
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='user')
    async def user_command(self, ctx, membro: discord.Member = None):
        membro = membro or ctx.author
        user_id = membro.id
        user_name = membro.name
        avatar_url = membro.avatar.url if membro.avatar else membro.default_avatar.url

        # Caminho absoluto para o banco de dados
        db_path = os.path.join(os.path.dirname(__file__), '..', 'users', 'users.db')

        try:
            # Conectando ao banco de dados
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                # Verifica se o usuário já existe, senão insere
                cursor.execute("SELECT 1 FROM usuarios WHERE userId = ?", (user_id,))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO usuarios (userId) VALUES (?)", (user_id,))
                    conn.commit()

                # Busca os dados do usuário
                cursor.execute(
                    "SELECT userXp, userLevel, userWallet FROM usuarios WHERE userId = ?",
                    (user_id,)
                )
                result = cursor.fetchone()

                if result and all(r is not None for r in result):
                    xp, level, wallet = result
                else:
                    print(f"[ALERTA] Dados incompletos para o usuário {user_id}.")
                    xp = level = wallet = 0

        except Exception as e:
            print(f"[ERRO] ao acessar banco de dados: {e}")
            await ctx.send("❌ Erro ao acessar os dados do usuário.")
            return

        # Monta o embed com as informações do usuário
        embed = discord.Embed(
            title=f"📋 Perfil de {user_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔢 Nível", value=str(level), inline=True)
        embed.add_field(name="⭐ XP", value=str(xp), inline=True)
        embed.add_field(name="💰 Créditos", value=f"{wallet} créditos", inline=True)
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(User(bot))
