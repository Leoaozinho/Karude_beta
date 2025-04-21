import discord
from discord.ext import commands
from Modules.Database.db_connection import DatabaseManager

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()

    @commands.command(name='user')
    async def user_command(self, ctx):
        userId = ctx.author.id
        userName = ctx.author.name
        userAvatar = ctx.author.avatar.url if ctx.author.avatar else "https://cdn-icons-png.flaticon.com/512/1695/1695213.png"

        # Verifica ou cria o usuário no banco
        self.db.ensure_user_exists(userId)
        userInfo = self.db.get_user_info(userId)

        embed = discord.Embed(
            title=f"Informações do {userName}",
            description=userInfo,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=userAvatar)
        embed.set_footer(text=f"Solicitado por {userName}", icon_url=userAvatar)

        await ctx.send(embed=embed)

    def cog_unload(self):
        self.db.close()