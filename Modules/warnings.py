import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conexao = sqlite3.connect("user.db")
        self.cursor = self.conexao.cursor()

class SistemaAvisos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conexao = ...  # sua conexão sqlite
        self.cursor = self.conexao.cursor()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisar(self, ctx, membro: discord.Member, *, motivo: str):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cursor.execute("INSERT INTO warnings (user_id, mod_id, motivo, data) VALUES (?, ?, ?, ?)",
                            (membro.id, ctx.author.id, motivo, data))
        self.conexao.commit()

        # Contar número total de avisos do usuário
        self.cursor.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ?", (membro.id,))
        total_avisos = self.cursor.fetchone()[0]

        await ctx.send(f"{membro.mention} recebeu um aviso: **{motivo}** (Total: {total_avisos})")

        # Aplica punição automática se necessário
        await self.aplicar_punicao(ctx, membro, total_avisos)

    async def aplicar_punicao(self, ctx, membro: discord.Member, total_avisos: int):
        try:
            if total_avisos == 3:
                # Timeout de 1 hora
                duration = timedelta(hours=1)
                await membro.timeout(duration, reason="Acumulou 3 avisos")
                await ctx.send(f"{membro.mention} foi silenciado por 1 hora por atingir 3 avisos.")

            elif total_avisos == 4:
                await membro.kick(reason="Acumulou 4 avisos")
                await ctx.send(f"{membro.mention} foi expulso do servidor por atingir 4 avisos.")

            elif total_avisos >= 5:
                await membro.ban(reason="Acumulou 5 ou mais avisos")
                await ctx.send(f"{membro.mention} foi banido do servidor por reincidência.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para aplicar a punição.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao aplicar a punição: {e}")
    
    

    @commands.command()
    async def avisos(self, ctx, membro: discord.Member):
        self.cursor.execute("SELECT motivo, data FROM warnings WHERE user_id = ?", (membro.id,))
        avisos = self.cursor.fetchall()

        if not avisos:
            await ctx.send(f"{membro.mention} não possui nenhum aviso.")
        else:
            embed = discord.Embed(title=f"Avisos de {membro}", color=discord.Color.orange())
            for idx, (motivo, data) in enumerate(avisos, start=1):
                embed.add_field(name=f"Aviso {idx}", value=f"**Motivo:** {motivo}\n📅 {data}", inline=False)
            await ctx.send(embed=embed)

# Função de setup obrigatória para o bot carregar o cog
async def setup(bot):
    await bot.add_cog(Warnings(bot))