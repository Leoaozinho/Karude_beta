from discord.ext import commands
import discord
import sqlite3
import os

# Função para obter informações do usuário no banco de dados
def info_user(user_id):
    db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT userId, userXp, userLevel, userWallet FROM usuarios WHERE userId = ?", (user_id,))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        userId, userXp, userLevel, userWallet = usuario
        message = (f"XP: {userXp}\nNível: {userLevel}\nMoedas: {userWallet}\n")
        return message
    else:
        return "Usuário não encontrado no banco de dados."

# Cog com o comando para exibir informações do usuário
class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='user')
    async def user_command(self, ctx):
        user_id = int(ctx.author.id)
        user_name = ctx.author.name
        user_avatar_url = ctx.author.avatar.url if ctx.author.avatar else "https://cdn-icons-png.flaticon.com/512/1695/1695213.png"

        # Pega informações do usuário no banco de dados
        user_info = info_user(user_id)

        # Cria o embed
        embed = discord.Embed(
            title=f"Informações do {user_name}",
            description=user_info,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user_avatar_url)
        embed.set_footer(text=f"Solicitado por {user_name}", icon_url=user_avatar_url)

        # Envia o embed
        await ctx.send(embed=embed)

# Função de setup para adicionar o Cog ao bot
async def setup(bot: commands.Bot):
    await bot.add_cog(User(bot))
