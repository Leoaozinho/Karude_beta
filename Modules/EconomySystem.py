from discord.ext import commands
import json
import os
from datetime import datetime, timedelta


class EconomySystem(commands.Cog):
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
            self.economy_data[user_id] = {"balance": 0, "last_daily": None}
        self.economy_data[user_id]["balance"] += amount
        self.save_data()

    @commands.command(name='daily')
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        self.load_data()  # Reload data to get the most up-to-date information

        now = datetime.utcnow()
        last_daily = self.economy_data.get(user_id, {}).get("last_daily")

        if last_daily:
            last_daily = datetime.strptime(last_daily, "%Y-%m-%d %H:%M:%S")
            if now - last_daily < timedelta(days=1):
                remaining_time = timedelta(days=1) - (now - last_daily)
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await ctx.send(
                    f'{ctx.author.mention}, você já coletou seus créditos diários! Tente novamente em {hours}h {minutes}m {seconds}s.')
                return

        self.update_balance(user_id, 150)
        self.economy_data[user_id]["last_daily"] = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.save_data()

        await ctx.send(f'{ctx.author.mention}, você recebeu 150 créditos diários!')


async def setup(bot):
    await bot.add_cog(EconomySystem(bot))
