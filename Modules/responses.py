import random
from typing import Any

from discord.ext import commands

# Dicionário de respostas automáticas
AUTOMATIC_RESPONSES = {
    'hello': ['Hello!', 'Hi there!', 'Greetings!'],
    'how are you': ['I\'m a bot, I\'m always fine!', 'Doing great, thanks!', 'Can\'t complain!'],
    # Adicione mais respostas automáticas conforme necessário
}


def get_response(user_input: str) -> Any | None:
    """
    Função para obter uma resposta com base na entrada do usuário.
    """
    lowered = user_input.lower()
    for key in AUTOMATIC_RESPONSES:
        if key in lowered:
            return random.choice(AUTOMATIC_RESPONSES[key])
    return None


def setup(bot):
    """
    Configuração do bot para adicionar o evento de mensagem automática.
    """

    @bot.event
    async def on_message(message):
        # Ignorar mensagens de outros bots
        if message.author.bot:
            return

        # Obter resposta automática, se existir
        response = get_response(message.content)
        if response:
            await message.channel.send(response)

        # Processar outros comandos que o bot possa ter
        await bot.process_commands(message)
