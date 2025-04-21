import discord
from discord.ext import commands

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1363985537165430874  # Substitua com o ID real

    async def log(self, message: str):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            try:
                await channel.send(message)
            except Exception as e:
                print(f"[Erro ao enviar log] {e}")
        else:
            print(f"[Logger] Canal de log com ID {self.log_channel_id} não encontrado.")

    # Membro entrou
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log(f"🟢 **{member} entrou no servidor.**")

    # Membro saiu
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log(f"🔴 **{member} saiu do servidor.**")

    # Comando importante usado
    @commands.Cog.listener()
    async def on_command(self, ctx):
        important_commands = ['slots', 'daily', 'registro', 'trivia']
        if ctx.command and ctx.command.name in important_commands:
            canal_nome = ctx.channel.name if hasattr(ctx.channel, 'name') else 'DM'
            await self.log(
                f"📢 **{ctx.author}** usou o comando `!{ctx.command.name}` no canal **#{canal_nome}**."
            )

    # Mensagem editada
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        canal_nome = before.channel.name if hasattr(before.channel, 'name') else 'DM'
        await self.log(
            f"✏️ **Mensagem editada por {before.author} em #{canal_nome}**\n"
            f"**Antes:** {before.content}\n"
            f"**Depois:** {after.content}"
        )

    # Mensagem deletada
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        canal_nome = message.channel.name if hasattr(message.channel, 'name') else 'DM'
        await self.log(
            f"🗑️ **Mensagem deletada por {message.author} em #{canal_nome}**\n"
            f"**Conteúdo:** {message.content}"
        )

    # Membro banido
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.log(f"🔨 **{user} foi banido do servidor {guild.name}.**")

    # Membro desbanido
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await self.log(f"⚖️ **{user} foi desbanido do servidor {guild.name}.**")

# Setup
async def setup(bot):
    await bot.add_cog(Logger(bot))