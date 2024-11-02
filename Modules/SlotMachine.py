import random
import discord
from discord.ext import commands
import os
import json

class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_data()
        self.accumulated_prize = 0  # Variável para armazenar os créditos acumulados

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

        # Enviar GIF antes do embed
        slot_machine_gif_url = 'https://giphy.com/gifs/transparent-pokemon-dGD5YHl8xW6c'  # Substitua pelo URL do GIF
        await ctx.send(slot_machine_gif_url)

        # Os símbolos do Slot Machine
        symbols = ["🍒", "🍋", "🍉", "🍇", "🍓"]
        slots = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]

        # Criação do embed para mostrar os slots
        embed = discord.Embed(
            title="Slot Machine",
            description=f"{slots[0][0]} | {slots[0][1]} | {slots[0][2]}\n"
                        f"{slots[1][0]} | {slots[1][1]} | {slots[1][2]}\n"
                        f"{slots[2][0]} | {slots[2][1]} | {slots[2][2]}",
            color=discord.Color.gold()
        )

        # Verifica se o jogador ganhou algo
        def check_win(slot):
            return (slot[0] == slot[1] == slot[2] or  # Horizontal
                    [slot[0][0], slot[1][1], slot[2][2]] == [slot[0][2], slot[1][1], slot[2][0]] or  # Diagonal
                    [slot[0][0], slot[1][0], slot[2][0]] == [slot[0][1], slot[1][1], slot[2][1]] == [slot[0][2], slot[1][2], slot[2][2]])  # Vertical

        if check_win(slots):
            prize = 100 + self.accumulated_prize  # Adiciona o valor acumulado ao prêmio
            embed.add_field(name="Resultado", value=f"Parabéns! Você ganhou {prize} créditos!")
            self.update_balance(user_id, prize)
            print(
                f'Adicionado {prize} créditos para {ctx.author.name}. Saldo atual: '
                f'{self.economy_data[user_id]["balance"]}')  # Debug
            self.accumulated_prize = 0  # Reseta o valor acumulado após a vitória
        else:
            embed.add_field(name="Resultado", value="Que pena! Você não ganhou desta vez. Tente novamente!")
            self.accumulated_prize += 25  # Acumula os créditos que o jogador perdeu

        await ctx.send(embed=embed)

# Para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(SlotMachine(bot))
