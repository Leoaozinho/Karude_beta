import random
from discord.ext import commands


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

        # Mostra o resultado ao jogador
        result_str = "".join(result)
        await ctx.send(f"Resultado: {result_str}")

        # Verifica se houve algum prêmio
        prize = prize_levels.get(result_str, 0)
        if prize > 0:
            await ctx.send(f"Parabéns! Você ganhou {prize} pontos!")
            self.difficulty += 1  # Aumenta a dificuldade
        else:
            await ctx.send("Não foi dessa vez! Tente novamente.")
            if self.difficulty > 1:
                self.difficulty -= 1  # Diminui a dificuldade


# Função setup para adicionar o cog
async def setup(bot):
    await bot.add_cog(SlotMachine(bot))
    