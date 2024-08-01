from discord.ext import commands
import discord

class Socorro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='socorro')
    async def socorro_command(self, ctx, *args):
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
            embed.title = "Comandos Disponíveis"
            embed.description = ('Digite !socorro comandos para ver os comandos que eu sei <:actually:1263690743864758395>\n'
                                 'Digite !socorro falas para ver as falas que eu respondo quando chamada <:1b:1259507885948534896>')
            return embed

        if 'falas' in lowered:
            embed.title = "Falas Disponíveis"
            embed.description = ('Eu consigo responder:\n'
                                 '- bom dia\n'
                                 '- você esta?\n'
                                 '- tu esta?\n'
                                 '- ouvindo\n'
                                 '- está bem?\n'
                                 '- esta fazendo?\n'
                                 '- oi\n'
                                 '- tudo bem?\n'
                                 '- tchau\n'
                                 '- academia\n'
                                 '- trilha favorita\n\n'
                                 'Qualquer ideia de implementação ou melhoria, fale com os meus desenvolvedores OwO')
            return embed
        elif 'comandos' in lowered:
            embed.title = "Comandos Disponíveis"
            embed.description = ('Os comandos que eu aprendi são:\n'
                                 '- socorro\n'
                                 '- trivia\n'
                                 '- slot\n'
                                 '- falas\n'
                                 '- dadottttttttttttttttttttttttttttttttt 4\n'
                                 '- dado 6\n'
                                 '- dado 8\n'
                                 '- dado 10\n'
                                 '- dado 12\n'
                                 '- dado 20\n'
                                 '- dado 100\n'
                                 '- comandos\n\n'
                                 'Qualquer ideia de implementação ou melhoria, fale com os meus desenvolvedores OwO')
            return embed

        return None

async def setup(bot: commands.Bot):
    await bot.add_cog(Socorro(bot))
