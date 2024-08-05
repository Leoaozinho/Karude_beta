import discord
from discord.ext import commands
import json


class EconomySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_data()

    def load_data(self):
        """Load user and shop data from JSON files."""
        self.xp_data = self.load_json('xp_data.json')
        self.economy_data = self.load_json('economy_data.json')
        self.shop_items = self.load_json('shop_items.json')
        self.user_inventory = self.load_json('user_inventory.json')

    def load_json(self, filename):
        """Load a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

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
    async def buy(self, ctx, item_id: str):
        """Purchase an item from the shop."""
        user_id = str(ctx.author.id)

        # Load item details
        item = next((item for item in self.shop_items if item['id'] == item_id), None)
        if not item:
            await ctx.send("Item não encontrado!")
            return

        # Load user data
        money = self.economy_data.get(user_id, {"money": 0})
        user_money = money.get("money", 0)

        if user_money < item['price']:
            await ctx.send("Você não tem dinheiro suficiente para comprar este item.")
            return

        # Deduct money
        user_money -= item['price']
        money['money'] = user_money
        self.economy_data[user_id] = money
        self.save_json('economy_data.json', self.economy_data)

        # Update user inventory
        inventory = self.user_inventory.get(user_id, [])
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
