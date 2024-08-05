import discord
from discord.ext import commands
from random import choice
import os
from dotenv import load_dotenv

load_dotenv()

WELCOME_CHANNEL = os.getenv('WELCOME_CHANNEL_ID')
CARGOS_CHANNEL = os.getenv('CARGOS_CHANNEL_ID')
REGRAS_CHANNEL = os.getenv('REGRAS_CHANNEL_ID')
GERAL_CHANNEL = os.getenv('GERAL_CHANNEL_ID')

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(choice([
                f"Seja bem-vindo(a) ao server, {member.mention}! <:1b:1259507885948534896> Fique à vontade para explorar e se divertir.",
                f"Fique à vontade {member.mention}, para explorar e se divertir! <:actually:1263690743864758395>",
                f"Olá {member.mention}, vava ou Twice? Eu curto os dois <:1b:1259507885948534896>",
                f"Welcome {member.mention} <:Mikohumf2:1259507775222976543>, por que não mando um olá no <#{GERAL_CHANNEL_ID}>? (～￣▽￣)～ ",
                f"Irasshaimase {member.mention} <:Ilustracao_Sem_Titulo2:1259507809922584647>, recomendo dar uma olhada nas <#{REGRAS_CHANNEL_ID}> (o′┏▽┓｀o)",
                f"Salve {member.mention} <:1b:1259507885948534896>, de uma olhada no canal de <#{CARGOS_CHANNEL_ID}> (≧︶≦))(￣▽￣ )ゞ",
                f"Bem vindo ao GC dos gurizes {member.mention} <:actually:1263690743864758395>, trouxe os refris? (￣y▽,￣)╭"
            ]))

async def setup(bot: commands.Bot):
    await bot.add_cog(BoasVindas(bot))
