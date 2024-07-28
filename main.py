import os
import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from Modules import registro
from Modules import boas_vindas
from Modules import jogo_quiz

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Inicializar o bot
client = commands.Bot(command_prefix="!", intents=intents)

# Carregar a extensão de respostas automáticas
try:
    bot.load_extension('modules.responses')  # Certifique-se de que o caminho está correto
except Exception as e:
    print(f'Erro ao carregar a extensão modules.responses: {e}')


@client.event
async def on_ready():
    print(f'{client.user} está online!')


# Registrar funcionalidades dos módulos
registro.setup(client)
boas_vindas.setup(client)
jogo_quiz.setup(client)
bot.load_extension('slot_machine')


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
