import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    for filename in os.listdir('./Modules'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'Modules.{filename[:-3]}')
                # print(f'{filename[:-3]} carregado com sucesso.')  # comente este print quando for pra versão live.
            except Exception as e:
                print(f'Falha ao carregar {filename[:-3]}: {e}')  # esse pode deixar, ele retorna erro quando existe.

    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Não conheço esse parâmetro, tenta usar o **!help**')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Esse comando não existe, tenta usar o **!help**')

bot.run(TOKEN)