import discord
from discord.ext import commands
import json
import os
import asyncio
from datetime import datetime, timedelta


class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_data()
        self.last_xp_time = {}

    def load_data(self):
        if not os.path.exists('economy_data.json'):
            with open('economy_data.json', 'w') as f:
                json.dump({}, f)

        with open('economy_data.json', 'r') as f:
            self.economy_data = json.load(f)

        if not os.path.exists('xp_data.json'):
            with open('xp_data.json', 'w') as f:
                json.dump({}, f)

        with open('xp_data.json', 'r') as f:
            self.xp_data = json.load(f)

    def save_data(self):
        with open('economy_data.json', 'w') as f:
            json.dump(self.economy_data, f)

        with open('xp_data.json', 'w') as f:
            json.dump(self.xp_data, f)

    def update_balance(self, user_id, amount):
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"balance": 0}
        self.economy_data[user_id]["balance"] += amount
        self.save_data()

    def update_xp(self, user_id, xp_amount, ctx):
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0, "level": 1}
        self.xp_data[user_id]["xp"] += xp_amount

        # Update level based on XP
        level = self.xp_data[user_id]["level"]
        xp = self.xp_data[user_id]["xp"]
        xp_for_next_level = 100 * (2 ** (level - 1))  # XP required doubles each level

        if xp >= xp_for_next_level:
            self.xp_data[user_id]["level"] += 1
            self.xp_data[user_id]["xp"] -= xp_for_next_level  # Carry over extra XP
            self.save_data()
            # Send level up message
            asyncio.create_task(self.send_level_up_message(ctx, self.xp_data[user_id]["level"]))

        self.save_data()

    async def send_level_up_message(self, ctx, new_level):
        await ctx.send(f"Parabéns {ctx.author.mention}, você subiu para o nível {new_level}! 🎉")

    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        self.load_data()  # Reload data to get the most up-to-date information

        user_id = str(member.id)
        xp_info = self.xp_data.get(user_id, {"xp": 0, "level": 1})
        balance_info = self.economy_data.get(user_id, {"balance": 0})

        # Create XP bar
        level = xp_info["level"]
        xp = xp_info["xp"]
        xp_for_next_level = 100 * (2 ** (level - 1))  # XP required doubles each level
        progress_bar_length = 20
        filled_length = int(progress_bar_length * xp / xp_for_next_level)
        progress_bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)

        embed = discord.Embed(
            title=f"Perfil de {member.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Nível", value=f"{level}", inline=False)
        embed.add_field(name="XP", value=f"{progress_bar} ({xp}/{xp_for_next_level})", inline=False)
        embed.add_field(name="Saldo", value=f"{balance_info['balance']} 💰", inline=False)
        embed.add_field(name="Inventário", value="Seu inventário está vazio.", inline=False)  # Placeholder

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        current_time = datetime.now()

        if user_id in self.last_xp_time:
            last_xp_time = self.last_xp_time[user_id]
            if current_time - last_xp_time < timedelta(minutes=2):
                return

        self.last_xp_time[user_id] = current_time
        self.update_xp(user_id, 20, message.channel)


async def setup(bot):
    await bot.add_cog(XPSystem(bot))
