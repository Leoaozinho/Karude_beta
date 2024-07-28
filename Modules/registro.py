import discord
from discord.ext import commands
import asyncio

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

REGISTRATION_CHANNEL_ID = 1266353703825313812  # Substitua pelo ID do seu canal de registro
NON_REGISTRATION_WARNINGS = {}

async def registro(ctx):
    if ctx.channel.id != REGISTRATION_CHANNEL_ID:
        user_warnings = NON_REGISTRATION_WARNINGS.get(ctx.author.id, 0)
        if user_warnings < 2:
            NON_REGISTRATION_WARNINGS[ctx.author.id] = user_warnings + 1
            warning_msg = await ctx.send("Este comando só pode ser usado no canal de registro.")
            await asyncio.sleep(10)
            await warning_msg.delete()
        return

    # Painel de Gênero
    embed_genero = discord.Embed(title="Escolha seu cargo de Gênero",
                                 description="Clique nas reações abaixo para selecionar seu cargo de gênero.")
    for emoji, role_name in ROLES_GENERO.items():
        embed_genero.add_field(name=emoji, value=role_name, inline=True)

    message_genero = await ctx.send(embed=embed_genero)
    for emoji in ROLES_GENERO.keys():
        await message_genero.add_reaction(emoji)

    # Painel de Trilhas
    embed_trilhas = discord.Embed(title="Escolha seu cargo de Trilha",
                                  description="Clique nas reações abaixo para selecionar seu cargo de trilha.")
    for emoji, role_name in ROLES_TRILHAS.items():
        embed_trilhas.add_field(name=emoji, value=role_name, inline=True)

    message_trilhas = await ctx.send(embed=embed_trilhas)
    for emoji in ROLES_TRILHAS.keys():
        await message_trilhas.add_reaction(emoji)

    # Apagar as mensagens após 40 segundos
    await asyncio.sleep(40)
    await ctx.message.delete()
    await message_genero.delete()
    await message_trilhas.delete()

async def on_reaction_add(reaction, user):
    if user == reaction.message.guild.me:
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)

    if reaction.emoji in ROLES_GENERO:
        role_name = ROLES_GENERO[reaction.emoji]
        new_role = discord.utils.get(guild.roles, name=role_name)

        if new_role:
            for role in member.roles:
                if role.name in ROLES_GENERO.values():
                    await member.remove_roles(role)
            await member.add_roles(new_role)

    elif reaction.emoji in ROLES_TRILHAS:
        role_name = ROLES_TRILHAS[reaction.emoji]
        new_role = discord.utils.get(guild.roles, name=role_name)

        if new_role:
            for react in reaction.message.reactions:
                if react.emoji in ROLES_TRILHAS and react != reaction:
                    async for user_in_react in react.users():
                        if user_in_react == user:
                            await reaction.message.remove_reaction(react.emoji, user)
                            break
            await member.add_roles(new_role)

async def on_reaction_remove(reaction, user):
    if user == reaction.message.guild.me:
        return

    guild = reaction.message.guild
    member = guild.get_member(user.id)

    if reaction.emoji in ROLES_GENERO:
        role_name = ROLES_GENERO[reaction.emoji]
        role = discord.utils.get(guild.roles, name=role_name)

        if role and role in member.roles:
            await member.remove_roles(role)

    elif reaction.emoji in ROLES_TRILHAS:
        role_name = ROLES_TRILHAS[reaction.emoji]
        role = discord.utils.get(guild.roles, name=role_name)

        if role and role in member.roles:
            await member.remove_roles(role)

def setup(bot):
    bot.add_command(commands.Command(registro, name='registro'))
    bot.add_listener(on_reaction_add, 'on_reaction_add')
    bot.add_listener(on_reaction_remove, 'on_reaction_remove')
