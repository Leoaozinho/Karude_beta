import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1021536346298388491  # Substitua pelo ID do seu canal de boas-vindas


class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(
                f"Seja bem-vindo(a) ao servidor, {member.mention}! Fique à vontade para explorar e se divertir.")


async def setup(bot):
    await bot.add_cog(BoasVindas(bot))
