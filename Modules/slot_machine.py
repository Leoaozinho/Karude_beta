from discord.ext import commands
import random
import json

# Definir símbolos e valores
SLOT_MACHINE_SYMBOLS = {
    "🍒": 10,
    "🍋": 20,
    "🍊": 30,
    "🍉": 40,
    "🍇": 50,
    "⭐": 100
}

# Definir níveis de dificuldade
DIFFICULTY_LEVELS = {
    1: {"symbols": 3, "probability": 0.5},  # Fácil
    2: {"symbols": 2, "probability": 0.4},  # Médio
    3: {"symbols": 1, "probability": 0.3}  # Difícil
}

# Inicializar o banco de dados de pontos e dificuldades
points_file = 'points.json'
difficulty_file = 'difficulty.json'


def load_points():
    try:
        with open(points_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_points(points):
    with open(points_file, 'w') as f:
        json.dump(points, f)


def load_difficulty():
    try:
        with open(difficulty_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_difficulty(difficulty):
    with open(difficulty_file, 'w') as f:
        json.dump(difficulty, f)


# Função para girar a slot machine com dificuldade dinâmica
def spin_slot_machine(level):
    difficulty = DIFFICULTY_LEVELS[level]
    symbols = list(SLOT_MACHINE_SYMBOLS.keys())
    result = [random.choice(symbols) for _ in range(difficulty["symbols"])]

    # Checar se o resultado é uma combinação vencedora
    if random.random() <= difficulty["probability"]:
        return result, True
    else:
        return result, False


# Comando de slot machine
class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='slot')
    async def slot(self, ctx, bet: int = 10):
        points = load_points()
        difficulty = load_difficulty()
        user_id = str(ctx.author.id)

        if user_id not in points:
            points[user_id] = 100  # Pontos iniciais

        if user_id not in difficulty:
            difficulty[user_id] = 1  # Dificuldade inicial

        if bet > points[user_id]:
            await ctx.send("Você não tem pontos suficientes para essa aposta.")
            return

        # Girar a slot machine com base na dificuldade atual
        level = difficulty[user_id]
        result, win = spin_slot_machine(level)
        result_str = ' | '.join(result)

        if win:
            prize = sum(SLOT_MACHINE_SYMBOLS[symbol] for symbol in result)
            points[user_id] += prize - bet  # Ganho de pontos
            await ctx.send(f"🎰 {result_str} 🎰\nVocê ganhou {prize - bet} pontos! Total de pontos: {points[user_id]}")
            # Aumentar a dificuldade
            difficulty[user_id] = min(level + 1, len(DIFFICULTY_LEVELS))
        else:
            points[user_id] -= bet  # Perda de pontos
            await ctx.send(f"🎰 {result_str} 🎰\nTente novamente! Total de pontos: {points[user_id]}")
            # Diminuir a dificuldade se necessário
            difficulty[user_id] = max(level - 1, 1)

        save_points(points)
        save_difficulty(difficulty)

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        points = load_points()
        sorted_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
        leaderboard = "\n".join([f"<@{user_id}>: {pts} pontos" for user_id, pts in sorted_points])
        await ctx.send(f"**Leaderboard**\n{leaderboard}")


# Função setup para registrar o comando
async def setup(bot):
    await bot.add_cog(SlotMachine(bot))
