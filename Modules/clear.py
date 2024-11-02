import discord
from discord.ext import commands
import time

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    async def clear_command(self, ctx, number: int):
        cargo_id = 1263827423569645710

        cargo = discord.utils.get(ctx.guild.roles, id=cargo_id)
        if cargo in ctx.author.roles:
            await ctx.channel.purge(limit=number+1)
            time.sleep(1)
            await ctx.send(f"{str(number)} mensagens deletadas")

async def setup(bot: commands.Bot):
    await bot.add_cog(clear(bot))