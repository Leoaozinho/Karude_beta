from random import randint
from discord.ext import commands
import discord

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
            embed.description = ('Você pode rolar diferentes tipos de dados, basta digitar `!dado` seguido de:\n'
                                 '- dado 4\n'
                                 '- dado 6\n'
                                 '- dado 8\n'
                                 '- dado 10\n'
                                 '- dado 12\n'
                                 '- dado 20\n'
                                 '- dado 100')
            return embed

        if '100' in lowered:
            embed.title = "Rolagem de d100"
            embed.description = f'Resultado: {randint(1, 100)} 🎲'
            return embed
        elif '20' in lowered:
            embed.title = "Rolagem de d20"
            embed.description = f'Resultado: {randint(1, 20)} 🎲'
            return embed
        elif '12' in lowered:
            embed.title = "Rolagem de d12"
            embed.description = f'Resultado: {randint(1, 12)} 🎲'
            return embed
        elif '10' in lowered:
            embed.title = "Rolagem de d10"
            embed.description = f'Resultado: {randint(1, 10)} 🎲'
            return embed
        elif '8' in lowered:
            embed.title = "Rolagem de d8"
            embed.description = f'Resultado: {randint(1, 8)} 🎲'
            return embed
        elif '6' in lowered:
            embed.title = "Rolagem de d6"
            embed.description = f'Resultado: {randint(1, 6)} 🎲'
            return embed
        elif '4' in lowered:
            embed.title = "Rolagem de d4"
            embed.description = f'Resultado: {randint(1, 4)} 🎲'
            return embed

        return None

async def setup(bot: commands.Bot):
    await bot.add_cog(Dado(bot))
    print("Comando dado registrado.")
