import discord
from discord.ext import commands
from Modules.Database.db_connection import DatabaseConnection

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseConnection()

@commands.command(name='user')
async def user_command(self, ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    userId = membro.id
    userName = membro.name
    avatar = membro.avatar.url if membro.avatar else membro.default_avatar.url

    try:
        self.db.ensure_user_exists(userId)
        result = self.db.get_user_info(userId)

        if result and all(r is not None for r in result):
            xp, nivel, saldo = result
        else:
            print(f"[ALERTA] Dados incompletos ou ausentes para o usuário {userId}.")
            xp = nivel = saldo = 0

    except Exception as e:
        print(f"[ERRO] ao buscar dados do usuário {userId}: {e}")
        await ctx.send("❌ Ocorreu um erro ao buscar os dados do usuário.")
        return

    embed = discord.Embed(
        title=f"📋 Perfil de {userName}",
        color=discord.Color.blue()
    )
    embed.add_field(name="🔢 Nível", value=str(nivel), inline=True)
    embed.add_field(name="⭐ XP", value=str(xp), inline=True)
    embed.add_field(name="💰 Créditos", value=f"{saldo} créditos", inline=True)
    embed.set_thumbnail(url=avatar)
    embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)

    await ctx.send(embed=embed)

    def cog_unload(self):
        self.db.close()

async def setup(bot):
    await bot.add_cog(User(bot))