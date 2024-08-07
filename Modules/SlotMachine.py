import discord
from discord.ext import commands
import random
import json
import os


class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_data()

    def load_data(self):
        if not os.path.exists('economy_data.json'):
            with open('economy_data.json', 'w') as f:
                json.dump({}, f)

        with open('economy_data.json', 'r') as f:
            self.economy_data = json.load(f)

    def save_data(self):
        with open('economy_data.json', 'w') as f:
            json.dump(self.economy_data, f)

    def update_balance(self, user_id, amount):
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}
        self.economy_data[user_id]["balance"] += amount
        self.save_data()

    @commands.command(name='slots')
    async def slots(self, ctx):
        user_id = str(ctx.author.id)

        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}

        if self.economy_data[user_id]["balance"] < 25:
            await ctx.send(
                f'{ctx.author.mention}, você não tem créditos suficientes para jogar. Você precisa de 25 créditos.')
            return

        # Deduz 25 créditos
        self.update_balance(user_id, -25)
        print(
            f'Deduzido 25 créditos de {ctx.author.name}. Saldo atual: {self.economy_data[user_id]["balance"]}')  # Debug

        # Os símbolos do Slot Machine
        symbols = ["🍒", "🍋", "🍉", "🍇", "🍓"]
        slots = [random.choice(symbols) for _ in range(3)]

        # Criação do embed para mostrar os slots
        embed = discord.Embed(
            title="Slot Machine",
            description=f"{slots[0]} | {slots[1]} | {slots[2]}",
            color=discord.Color.gold()
        )

        # Verifica se o jogador ganhou algo
        if slots[0] == slots[1] == slots[2]:
            prize = 100
            embed.add_field(name="Resultado", value=f"Parabéns! Você ganhou {prize} créditos!")
            self.update_balance(user_id, prize)
            print(
                f'Adicionado {prize} créditos para {ctx.author.name}. Saldo atual: '
                f'{self.economy_data[user_id]["balance"]}')  # Debug
        else:
            embed.add_field(name="Resultado", value="Que pena! Você não ganhou desta vez. Tente novamente!")

        await ctx.send(embed=embed)


# Para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(SlotMachine(bot))
