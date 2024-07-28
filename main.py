import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from Modules import registro
from Modules import boas_vindas

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Inicializar o bot
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} está online!')


# Registrar funcionalidades dos módulos
registro.setup(client)
boas_vindas.setup(client)


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()
