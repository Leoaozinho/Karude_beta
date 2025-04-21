import discord
from discord.ext import commands
from datetime import datetime
import os
import sqlite3

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Define caminho absoluto até a pasta Database
        base_dir = os.path.dirname(os.path.dirname(__file__))  # Sobe para a pasta Modules
        db_dir = os.path.join(base_dir, "Database")
        os.makedirs(db_dir, exist_ok=True)  # Garante que a pasta exista

        db_path = os.path.join(db_dir, "user.db")  # Caminho final do banco
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Criação da tabela welcome_config se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS welcome_config (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        ''')
        self.conn.commit()

    @commands.command(name='setboasvindas')
    @commands.has_permissions(administrator=True)
    async def set_boas_vindas(self, ctx, canal_id: int):
        self.cursor.execute(
            "REPLACE INTO welcome_config (guild_id, channel_id) VALUES (?, ?)",
            (ctx.guild.id, canal_id)
        )
        self.conn.commit()
        await ctx.send(f"✅ Canal de boas-vindas definido com sucesso: <#{canal_id}>")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.cursor.execute("SELECT channel_id FROM welcome_config WHERE guild_id = ?", (member.guild.id,))
        resultado = self.cursor.fetchone()

        if resultado:
            channel_id = resultado[0]
            canal = self.bot.get_channel(channel_id)

            if canal:
                embed = discord.Embed(
                    title=f"Bem-vindo(a), {member.name}!",
                    description="Fique à vontade no servidor e bons estudos! 🥳",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.set_footer(text=f"ID: {member.id}")
                await canal.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BoasVindas(bot))