from random import randint
from discord.ext import commands
import discord
import re

class Dado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dado')
    async def dado_command(self, ctx, *args):
        user_message = ' '.join(args)
        embed = self.get_response_embed(user_message)

        # Verifica se o embed é válido
        if embed:
            try:
                await ctx.send(embed=embed)
            except discord.errors.HTTPException as e:
                # Log específico para erro HTTP
                print(f'Erro HTTP ao enviar mensagem: {e}')
            except Exception as e:
                # Log para outros tipos de erros
                print(f'Erro ao enviar mensagem: {e}')
        else:
            print('(Resposta vazia não enviada)')

    def get_response_embed(self, user_input: str) -> discord.Embed:
        lowered = user_input.lower()
        embed = discord.Embed(color=discord.Color.blue())

        if lowered == '':
            embed.title = "Tipos de Dados"
            embed.description = ('Você pode rolar diferentes tipos de dados, basta digitar `!dado` seguido de um número:\n'
                                 '- dado 4\n'
                                 '- dado 6\n'
                                 '- dado 8\n'
                                 '- dado 10\n'
                                 '- dado 12\n'
                                 '- dado 20\n'
                                 '- dado 100'
                                 '\n...')
            return embed
        
        match_number=re.search(r'\d+', lowered).group()
        embed.title = f"Rolagem de {match_number}"
        embed.description = f'Resultado: {randint(1, int(match_number))} 🎲'
        return embed

async def setup(bot: commands.Bot):
    await bot.add_cog(Dado(bot))
    print("Comando dado registrado.")