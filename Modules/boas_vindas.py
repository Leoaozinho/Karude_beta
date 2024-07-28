import discord
from discord.ext import commands

WELCOME_CHANNEL_ID = 1021536346298388491

async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"Seja bem-vindo(a) ao server, {member.mention}! Fique à vontade para explorar e se divertir!")

def setup(bot):
    bot.add_listener(on_member_join, 'on_member_join')
