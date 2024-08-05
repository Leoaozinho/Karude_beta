import discord
from discord.ext import commands
import json
import os


class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_xp_data()

    def load_xp_data(self):
        if os.path.exists('xp_data.json'):
            with open('xp_data.json', 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_xp_data(self):
        with open('xp_data.json', 'w') as f:
            json.dump(self.xp_data, f)

    def add_xp(self, user_id, xp_amount):
        if str(user_id) not in self.xp_data:
            self.xp_data[str(user_id)] = {"xp": 0, "level": 1}

        self.xp_data[str(user_id)]['xp'] += xp_amount

        current_xp = self.xp_data[str(user_id)]['xp']
        current_level = self.xp_data[str(user_id)]['level']
        xp_for_next_level = 100 * current_level

        if current_xp >= xp_for_next_level:
            self.xp_data[str(user_id)]['level'] += 1
            self.xp_data[str(user_id)]['xp'] = current_xp - xp_for_next_level
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        leveled_up = self.add_xp(user_id, 10)  # Add 10 XP for each message

        if leveled_up:
            level = self.xp_data[str(user_id)]['level']
            await message.channel.send(f"Parabéns {message.author.mention}, você subiu para o nível {level}!")

        self.save_xp_data()

    @commands.command(name='rank')
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_data = self.xp_data.get(str(member.id), {"xp": 0, "level": 1})

        embed = discord.Embed(
            title=f"Rank de {member.display_name}",
            description=f"Nível: {user_data['level']}\nXP: {user_data['xp']}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(XPSystem(bot))
