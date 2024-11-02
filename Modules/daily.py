from discord.ext import commands
from datetime import datetime, timedelta
import time
import sqlite3
import os

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='daily')
    async def daily_command(self, ctx):
        user_id = ctx.author.id

        db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')
        conn = sqlite3.connect(db_path)

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT userWallet, lastMsg FROM usuarios WHERE userId = ?", (user_id,))
            dailyCheck = cursor.fetchone()
            
            if dailyCheck is None:
                await ctx.send(f"{ctx.author.mention}, a sua primeira mensagem vai ser um !daily? Não, tenta de novo.")
                return

            balance, lastDaily = dailyCheck

            atual_datetime = datetime.now()
            lastDaily_dt = datetime.strptime(lastDaily, '%Y-%m-%d %H:%M:%S')

            if atual_datetime - lastDaily_dt > timedelta(hours=24):
                if balance is not None:
                    novo_saldo = balance + 150
                    
                    cursor.execute("UPDATE usuarios SET userWallet = ?, lastMsg = ? WHERE userId = ?", 
                                   (novo_saldo, atual_datetime.strftime('%Y-%m-%d %H:%M:%S'), user_id))
                    conn.commit()
                    
                    await ctx.send(f"{ctx.author.mention}, você recebeu 150 créditos diários!")
                else:
                    await ctx.send(f"{ctx.author.mention}, você não possui saldo registrado, chama o ADM.")
            else:
                next_available = lastDaily_dt + timedelta(hours=24)
                remaining_time = next_available - atual_datetime

                hours_remaining = remaining_time.days * 24 + remaining_time.seconds // 3600
                minutes_remaining = (remaining_time.seconds % 3600) // 60

                await ctx.send(f"{ctx.author.mention}, você já coletou seus créditos diários! Tente novamente em {hours_remaining} horas e {minutes_remaining} minutos.")

        except sqlite3.Error as e:
            print(f'Erro ao adicionar usuário: {e}')

        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Daily(bot))