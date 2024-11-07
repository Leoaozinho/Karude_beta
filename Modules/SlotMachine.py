import discord
from discord.ext import commands
import random
import sqlite3
import os

def verify_shot(userID):
    db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT userWallet FROM usuarios WHERE userId = ?", (userID,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] > 25:
        return True
    else:
        return False

def update_wallet(userID, amount):
    db_path = os.path.join(os.path.dirname(__file__), '../users', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT userWallet FROM usuarios WHERE userId=?", (userID,))
        result = cursor.fetchone()

        if result:
            current_wallet = result[0]
            new_wallet = current_wallet + amount

            cursor.execute("UPDATE usuarios SET userWallet=? WHERE userId=?", (new_wallet, userID))
            conn.commit()
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Erro ao atualizar o saldo:", e)
        return False
    finally:
        conn.close()

class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accumulated_prize = 0

    @commands.command(name="slots")
    async def slots(self, ctx):
        if not verify_shot(ctx.author.id):
            await ctx.send(f"{ctx.author.mention}, você está sem saldo para jogar.")
            return

        update_wallet(ctx.author.id, -25)

        symbols = ["🍒", "🍋", "🍉", "🍇", "🍓"]
        slots = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
        embed = discord.Embed(
            title="Slot Machine",
            description=f"{slots[0][0]} | {slots[0][1]} | {slots[0][2]}\n"
                        f"{slots[1][0]} | {slots[1][1]} | {slots[1][2]}\n"
                        f"{slots[2][0]} | {slots[2][1]} | {slots[2][2]}",
            color=discord.Color.gold()
        )
        
        embed.set_image(url="https://media.giphy.com/media/dGD5YHl8xW6c/giphy.gif")

        def check_win(slots):
            for row in slots:
                if row[0] == row[1] == row[2]:
                    return True
            for col in range(3):
                if slots[0][col] == slots[1][col] == slots[2][col]:
                    return True
            return (slots[0][0] == slots[1][1] == slots[2][2]) or (slots[0][2] == slots[1][1] == slots[2][0])

        if check_win(slots):
            prize = 100 + self.accumulated_prize
            embed.add_field(name="Resultado", value=f"Parabéns! Você ganhou {prize} créditos!")
            update_wallet(ctx.author.id, prize)
            self.accumulated_prize = 0
        else:
            embed.add_field(name="Resultado", value="Que pena! Você não ganhou desta vez. Tente novamente!")
            self.accumulated_prize += 100

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SlotMachine(bot))