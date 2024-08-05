import random
from discord.ext import commands
import discord


class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.difficulty = 1  # Início com dificuldade 1

    @commands.command(name='slot')
    async def slot_machine(self, ctx):
        # Define as recompensas baseadas na dificuldade
        rewards = {
            1: ["🍒", "🍋", "🔔", "💎", "7️⃣"],
            2: ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍉"],
            3: ["🍒", "🍋", "🔔", "💎", "7️⃣", "🍉", "🍇"]
        }

        # Define os prêmios
        prize_levels = {
            "🍒🍒🍒": 10,
            "🍋🍋🍋": 20,
            "🔔🔔🔔": 30,
            "💎💎💎": 50,
            "7️⃣7️⃣7️⃣": 100
        }

        # Gera o resultado com base na dificuldade
        symbols = rewards.get(self.difficulty, rewards[1])
        result = [random.choice(symbols) for _ in range(3)]

        # Cria o embed
        embed = discord.Embed(
            title="🎰 Máquinas de Slot 🎰",
            description="Tente a sorte e veja se você ganhou!",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Resultado",
            value=f"{' | '.join(result)}",
            inline=False
        )

        # Verifica se houve algum prêmio
        result_str = "".join(result)
        prize = prize_levels.get(result_str, 0)
        if prize > 0:
            embed.add_field(
                name="🏆 Parabéns! 🏆",
                value=f"Você ganhou {prize} pontos!",
                inline=False
            )
            self.difficulty += 1  # Aumenta a dificuldade
        else:
            embed.add_field(
                name="<:badge5:1259507927732191335> Não foi dessa vez! <:badge5:1259507927732191335>",
                value="Tente novamente para ganhar prêmios!",
                inline=False
            )
            if self.difficulty > 1:
                self.difficulty -= 1  # Diminui a dificuldade

        # Envia o embed
        await ctx.send(embed=embed)


# Função setup para adicionar o cog
async def setup(bot):
    await bot.add_cog(SlotMachine(bot))
    print("Comando slot registrado.")
