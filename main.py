import os
import discord
from discord.ext import commands
from typing import Final
from dotenv import load_dotenv
import asyncio

# Carregar variáveis de ambiente
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Inicializar o bot
client = commands.Bot(command_prefix="!", intents=intents)

# Dicionários com roles e seus respectivos emojis
ROLES_GENERO = {
    "🏷️": "Ele/Dele",
    "🌸": "Ela/Dela",
    "🪐": "Elu/Delu",
}

ROLES_TRILHAS = {
    "☕": "Java",
    "🐍": "Python",
    "📈": "Gestão de Vendas",
    "🎨": "MKT e Design",
}

# ID do canal de boas-vindas (substitua pelo ID do seu canal)
WELCOME_CHANNEL_ID = 1021536346298388491  # Coloque aqui o ID do canal de boas-vindas


@client.event
async def on_ready() -> None:
    print(f'{client.user} está online!')

@client.event
async def on_member_join(member: discord.Member) -> None:
    # Obtém o canal de boas-vindas
    channel = client.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Seja bem-vindo(a) ao server, {member.mention}! Fique à vontade para explorar e se divertir!")


@client.command(name='registro')
async def registro(ctx):
    # Painel de Gênero
    embed_genero = discord.Embed(title="Escolha seu cargo de Gênero",
                                 description="Clique nas reações abaixo para selecionar seu cargo de gênero.")
    for emoji, role_name in ROLES_GENERO.items():
        embed_genero.add_field(name=emoji, value=role_name, inline=True)

    # Enviar e aguardar as reações do painel de gênero
    message_genero = await ctx.send(embed=embed_genero)
    for emoji in ROLES_GENERO.keys():
        await message_genero.add_reaction(emoji)

    # Painel de Trilhas
    embed_trilhas = discord.Embed(title="Escolha seu cargo de Trilha",
                                  description="Clique nas reações abaixo para selecionar seu cargo de trilha.")
    for emoji, role_name in ROLES_TRILHAS.items():
        embed_trilhas.add_field(name=emoji, value=role_name, inline=True)

    # Enviar e aguardar as reações do painel de trilhas
    message_trilhas = await ctx.send(embed=embed_trilhas)
    for emoji in ROLES_TRILHAS.keys():
        await message_trilhas.add_reaction(emoji)

    # Apagar as mensagens após 40 segundos
    await asyncio.sleep(40)
    await ctx.message.delete()  # Apaga a mensagem do comando !registro
    await message_genero.delete()  # Apaga o painel de gênero
    await message_trilhas.delete()  # Apaga o painel de trilhas


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user == client.user:
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)

    if reaction.emoji in ROLES_GENERO:
        role_name = ROLES_GENERO[reaction.emoji]
        new_role = discord.utils.get(guild.roles, name=role_name)

        if new_role:
            # Remover todos os cargos de gênero antes de adicionar o novo
            for role in member.roles:
                if role.name in ROLES_GENERO.values():
                    await member.remove_roles(role)

            # Adicionar o novo cargo de gênero
            await member.add_roles(new_role)

    elif reaction.emoji in ROLES_TRILHAS:
        role_name = ROLES_TRILHAS[reaction.emoji]
        new_role = discord.utils.get(guild.roles, name=role_name)

        if new_role:
            # Remover reações antigas desta mensagem para o usuário
            for react in reaction.message.reactions:
                if react.emoji in ROLES_TRILHAS and react != reaction:
                    async for user_in_react in react.users():
                        if user_in_react == user:
                            await reaction.message.remove_reaction(react.emoji, user)
                            break

            # Adicionar o novo cargo de trilha
            await member.add_roles(new_role)

@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    if user == client.user:
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)

    if reaction.emoji in ROLES_GENERO:
        role_name = ROLES_GENERO[reaction.emoji]
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            if role in member.roles:
                await member.remove_roles(role)
            # Opcional: Enviar mensagem de DM sobre a remoção do cargo, se desejar

    elif reaction.emoji in ROLES_TRILHAS:
        role_name = ROLES_TRILHAS[reaction.emoji]
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            if role in member.roles:
                await member.remove_roles(role)
            # Opcional: Enviar mensagem de DM sobre a remoção do cargo, se desejar

def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()
