import discord
from discord.ext import commands
import json

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_data()

    def load_data(self):
        """Load user data from JSON files."""
        self.xp_data = self.load_json('xp_data.json')
        self.economy_data = self.load_json('economy_data.json')

    def load_json(self, filename):
        """Load a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def calculate_xp_bar(self, xp_amount, level):
        """Calculate the XP bar representation."""
        # Assuming 100 XP per level
        xp_needed = level * 100
        xp_progress = xp_amount % 100
        xp_total = 100

        filled_length = int(20 * (xp_progress / xp_total))
        bar = '█' * filled_length + '░' * (20 - filled_length)

        return bar

    @commands.command(name='rank')
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        # Load XP and economy data for the user
        user_id = str(member.id)
        xp = self.xp_data.get(user_id, {"xp": 0, "level": 1})
        money = self.economy_data.get(user_id, {"money": 0})

        level = xp.get("level", 1)
        xp_amount = xp.get("xp", 0)
        money_amount = money.get("money", 0)

        # Calculate XP bar
        xp_bar = self.calculate_xp_bar(xp_amount, level)

        # Emoji para dinheiro
        money_emoji = '💰'

        # Create embed for rank
        embed = discord.Embed(
            title=f"Perfil de {member.display_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Nível", value=f"Level {level}", inline=False)
        embed.add_field(name="XP", value=f"{xp_amount}\n{xp_bar}", inline=False)
        embed.add_field(name="Saldo", value=f"{money_emoji} {money_amount}", inline=False)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)

# Para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(XPSystem(bot))