import discord
from discord.ext import commands
from datetime import datetime

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return  # Ignora bots

        canal_boas_vindas = discord.utils.get(member.guild.text_channels, name='👋boas-vindas')
        if canal_boas_vindas is None:
            return

        embed = discord.Embed(
            title="👋 Seja muito bem-vindo(a) ao KaruLabs!",
            description=f"{member.mention}, espero que se divirta e juntos aprendamos bastante!",
            color=discord.Color.green()
        )
        embed.add_field(name="📌 Dicas úteis", value="Use `!registro` para se identificar\nUse `!help` para ver todos os comandos", inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Entrou em {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        await canal_boas_vindas.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))