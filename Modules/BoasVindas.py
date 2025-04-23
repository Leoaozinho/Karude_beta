import os
import sqlite3
import discord
from discord.ext import commands

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Caminho absoluto para o banco de dados
        db_path = os.path.join(os.path.dirname(__file__), '..', 'users', 'users.db')

        # Abre a conexão com o banco e prepara o cursor
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    @commands.command(name='setboasvindas')
    @commands.has_permissions(administrator=True)
    async def set_boas_vindas(self, ctx, canal_id: int):
        """
        Define o canal de boas-vindas do servidor.
        Apenas administradores podem usar esse comando.
        """
        try:
            self.cursor.execute(
                "REPLACE INTO welcome_config (guild_id, channel_id) VALUES (?, ?)",
                (ctx.guild.id, canal_id)
            )
            self.conn.commit()
            await ctx.send(f"✅ Canal de boas-vindas definido com sucesso: <#{canal_id}>")
        except Exception as e:
            await ctx.send(f"❌ Erro ao definir o canal de boas-vindas: {e}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Evento chamado quando um novo membro entra no servidor.
        Envia a mensagem de boas-vindas no canal configurado.
        """
        try:
            self.cursor.execute(
                "SELECT channel_id FROM welcome_config WHERE guild_id = ?",
                (member.guild.id,)
            )
            resultado = self.cursor.fetchone()

            if resultado:
                channel_id = resultado[0]
                canal = self.bot.get_channel(channel_id)

                if canal:
                    embed = discord.Embed(
                        title=f"👋 Bem-vindo(a), {member.name}!",
                        description="Fique à vontade no servidor e bons estudos! 🥳",
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                    embed.set_footer(text=f"ID: {member.id}")
                    await canal.send(embed=embed)
        except Exception as e:
            print(f"[ERRO] ao enviar mensagem de boas-vindas: {e}")

    def cog_unload(self):
        self.conn.close()

# Função para registrar o Cog no bot
async def setup(bot):
    await bot.add_cog(BoasVindas(bot))