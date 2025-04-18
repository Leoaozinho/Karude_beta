import discord
from discord.ext import commands

class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 121312453892789 # <- ID do canal de logs

    async def log(self, message: str):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            await channel.send(message)

# Log de Entrada de Membros
@commands.Cog.listener()
async def on_member_join(self, member):
    await self.log(f"👤 {member.name} entrou no server")

# Log de Saída de Membros
@commands.Cog.listener()
async def on_member_remove(self, member):
    await self.log(f"👤 {member.name} saiu do server")

# Log de Comandos Importantes
@commands.Cog.listener()
async def on_commands(self, ctx):
    important_commands = ['slots','daily','registro','trivia']
    if ctx.command.name in important_commands:
        await self.logf(f"📢 {ctx.author} usou o comando `!{ctx.command.name}` no canal #{ctx.channel}.")

# Setup
async def setup(bot):
    await bot.add_cog(logger(bot))