from discord.ext import commands
import discord
from datetime import datetime, timedelta
from Modules.Database.db_connection import DatabaseConnection

class SistemaAvisos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseConnection()
        self.conn = self.db.conn
        self.cursor = self.db.cursor
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mod_id INTEGER NOT NULL,
                motivo TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        self.conn.commit()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def avisar(self, ctx, membro: discord.Member, *, motivo: str):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cursor.execute(
            "INSERT INTO warnings (user_id, mod_id, motivo, data) VALUES (?, ?, ?, ?)",
            (membro.id, ctx.author.id, motivo, data)
        )
        self.conn.commit()

        self.cursor.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ?", (membro.id,))
        total_avisos = self.cursor.fetchone()[0]

        await ctx.send(f"{membro.mention} recebeu um aviso: **{motivo}** (Total: {total_avisos})")
        await self.aplicar_punicao(ctx, membro, total_avisos)

    async def aplicar_punicao(self, ctx, membro: discord.Member, total_avisos: int):
        try:
            if total_avisos == 3:
                await membro.timeout(timedelta(hours=1), reason="Acumulou 3 avisos")
                await ctx.send(f"{membro.mention} foi silenciado por 1 hora.")

            elif total_avisos == 4:
                await membro.kick(reason="Acumulou 4 avisos")
                await ctx.send(f"{membro.mention} foi expulso do servidor.")

            elif total_avisos >= 5:
                await membro.ban(reason="Acumulou 5 ou mais avisos")
                await ctx.send(f"{membro.mention} foi banido por reincidência.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para aplicar a punição.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao aplicar a punição: {e}")

    @commands.command()
    async def avisos(self, ctx, membro: discord.Member):
        self.cursor.execute("SELECT motivo, data FROM warnings WHERE user_id = ?", (membro.id,))
        avisos = self.cursor.fetchall()

        if not avisos:
            await ctx.send(f"{membro.mention} não possui avisos.")
        else:
            embed = discord.Embed(title=f"Avisos de {membro}", color=discord.Color.orange())
            for idx, (motivo, data) in enumerate(avisos, 1):
                embed.add_field(name=f"Aviso {idx}", value=f"**Motivo:** {motivo}\n📅 {data}", inline=False)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SistemaAvisos(bot))
