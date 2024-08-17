import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class EconomySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_json('xp_data.json')
        self.economy_data = self.load_json('economy_data.json')
        self.shop_items = self.load_json('shop_items.json')
        self.user_inventory = self.load_json('user_inventory.json')
        self.load_data()

    def load_json(self, file_path):
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r') as f:
            return json.load(f)

    def load_data(self):
        if not os.path.exists('economy_data.json'):
            with open('economy_data.json', 'w') as f:
                json.dump({}, f)

        with open('economy_data.json', 'r') as f:
            self.economy_data = json.load(f)

    def save_data(self):
        with open('economy_data.json', 'w') as f:
            json.dump(self.economy_data, f)

    def save_json(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def update_balance(self, user_id, amount):
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0, "last_daily": None}
        self.economy_data[user_id]["balance"] += amount
        self.save_data()

    @commands.command(name='daily')
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        self.load_data() # Reload data to get the most up-to-date information

        now = datetime.utcnow()
        last_daily = self.economy_data.get(user_id, {}).get("last_daily")

        if last_daily:
            try:
                last_daily = datetime.strptime(last_daily, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                last_daily = datetime.strptime(last_daily, "%Y-%m-%d %H:%M:%S.%f")

            if now - last_daily < timedelta(days=1):
                remaining_time = timedelta(days=1) - (now - last_daily)
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(
                    f'{ctx.author.mention}, você já coletou seus créditos diários! Tente novamente em {hours}h {minutes}m {seconds}s.')
                return

        # Conceder créditos diários e salvar o tempo atual
        self.update_balance(user_id, 150) # Atualizar o saldo do usuário
        self.economy_data[user_id]["last_daily"] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.save_data() # Salvar os dados atualizados

        await ctx.send(f'{ctx.author.mention}, você recebeu 150 créditos diários!')

    @commands.command(name='shop')
    async def shop(self, ctx):
        """Display the shop items."""
        embed = discord.Embed(
            title="Loja",
            description="Veja os itens disponíveis para compra:",
            color=discord.Color.green()
        )

        for item in self.shop_items:
            embed.add_field(
                name=f"{item['name']} - ${item['price']}",
                value=item['description'],
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name='buy')
    async def buy(self, ctx, *args):
        """Purchase an item from the shop."""
        user_id = str(ctx.author.id)
        user_message = ' '.join(args)

        item = next((item for item in self.shop_items if item['name'] == user_message), None)
        if not item:
            await ctx.send("Item não encontrado!")
            return

        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"money": 0, "balance": 0, "last_daily": 0}
            self.save_json('economy_data.json', self.economy_data)

        user = self.economy_data.get(user_id)
        user_money = user.get("money")

        if user_money < item['price']:
            await ctx.send("Você não tem dinheiro suficiente para comprar este item.")
            return

        # Deduct money
        user_money -= item['price']
        user['money'] = user_money
        self.economy_data[user_id] = user
        self.save_json('economy_data.json', self.economy_data)

        # Update user inventory
        if user_id not in self.user_inventory:
            self.user_inventory[user_id] = []
            self.save_json('user_inventory.json', self.user_inventory)

        inventory = self.user_inventory.get(user_id)
        inventory.append(item)
        self.user_inventory[user_id] = inventory
        self.save_json('user_inventory.json', self.user_inventory)

        await ctx.send(f"Você comprou {item['name']}!")

    @commands.command(name='inventory')
    async def inventory(self, ctx):
        """Display user's inventory."""
        user_id = str(ctx.author.id)
        inventory = self.user_inventory.get(user_id, [])

        if not inventory:
            await ctx.send("Seu inventário está vazio.")
            return

        embed = discord.Embed(
            title="Seu Inventário",
            description="Itens que você possui:",
            color=discord.Color.blue()
        )

        for item in inventory:
            embed.add_field(
                name=item['name'],
                value=item['description'],
                inline=False
            )

        await ctx.send(embed=embed)

# Para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(EconomySystem(bot))