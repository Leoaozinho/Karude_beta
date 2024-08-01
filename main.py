import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


async def load_extensions():
    initial_extensions = [
        'Modules.registro_cog',
        'Modules.BoasVindas',
        'Modules.JogoQuiz',
        'Modules.SlotMachine',
        'Modules.dado',
        'Modules.responses',
        'Modules.socorro'
    ]

    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await load_extensions()


bot.run('MTI2MzU4ODQwNzk1MTYyNjI4MA.GlcTW-.CUOSuJJoZgB30iGf9Nmi1_uC4kIoqhk8ZOFKkc')