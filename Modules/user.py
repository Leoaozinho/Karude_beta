import discord
from discord.ext import commands
from Modules.Database.db_connection import DatabaseConnection

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseConnection()

    @commands.command(name='user')
    async def user_command(self, ctx, member: discord.Member = None):
        target = member or ctx.author

        user_id = target.id
        user_name = target.name
        user_avatar = target.avatar.url if target.avatar else "https://cdn-icons-png.flaticon.com/512/1695/1695213.png"

        self.db.ensure_user_exists(user_id)
        user_info = self.db.get_user_info(user_id)

        embed = discord.Embed(
            title=f"Perfil de {user_name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user_avatar)
        embed.add_field(name="Nível", value=user_info["nivel"], inline=True)
        embed.add_field(name="XP", value=user_info["xp"], inline=True)
        embed.add_field(name="Saldo", value=f"💰 {user_info['saldo']}", inline=True)
        embed.set_footer(text=f"Solicitado por {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else user_avatar)

        await ctx.send(embed=embed)

    def cog_unload(self):
        self.db.close()

async def setup(bot):
    await bot.add_cog(User(bot))