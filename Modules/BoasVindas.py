import discord
from discord.ext import commands
from random import choice
import os
from dotenv import load_dotenv

load_dotenv()

class BoasVindas(commands.Cog):
    def init(self, bot):
        self.bot = bot
        self.welcome_channel_id = int(os.getenv('WELCOME_CHANNEL_ID'))
        self.cargos_channel_id = int(os.getenv('CARGOS_CHANNEL_ID'))
        self.regras_channel_id = int(os.getenv('REGRAS_CHANNEL_ID'))
        self.geral_channel_id = int(os.getenv('GERAL_CHANNEL_ID'))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(self.welcome_channel_id)
        if channel:
            await channel.send(choice([
                f"Seja bem-vindo(a) ao server, {member.mention}! :1b: Fique à vontade para explorar e se divertir.",
                f"Fique à vontade {member.mention}, para explorar e se divertir! :actually:",
                f"Olá {member.mention}, vava ou Twice? Eu curto os dois :1b:",
                f"Welcome {member.mention} :Mikohumf2:, por que não mando um olá no <#{self.geral_channel_id}>? (～￣▽￣)～ ",
                f"Irasshaimase {member.mention} :Ilustracao_Sem_Titulo2:, recomendo dar uma olhada nas <#{self.regras_channel_id}> (o′┏▽┓｀o)",
                f"Salve {member.mention} :1b:, de uma olhada no canal de <#{self.cargos_channel_id}> (≧︶≦))(￣▽￣ )ゞ",
                f"Bem vindo ao GC dos gurizes {member.mention} :actually:, trouxe os refris? (￣y▽,￣)╭"
            ]))

async def setup(bot: commands.Bot):
    await bot.add_cog(BoasVindas(bot))