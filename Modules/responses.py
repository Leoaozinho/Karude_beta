from random import choice
from discord import Message
from discord.ext import commands
import discord

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # Ignorar mensagens do próprio bot
        if message.author == self.bot.user:
            return

        user_message = message.content

        # Verifica se a mensagem está vazia
        if not user_message:
            print('(A mensagem estava vazia porque as intenções provavelmente não estavam ativadas)')
            return

        response = self.get_response(user_message)

        # Verifica se a resposta é None ou uma string vazia
        if response and response.strip():
            try:
                await message.channel.send(response)
            except discord.errors.HTTPException as e:
                # Log específico para erro HTTP
                print(f'Erro HTTP ao enviar mensagem: {e}')
            except Exception as e:
                # Log para outros tipos de erros
                print(f'Erro ao enviar mensagem: {e}')
        else:
            print('(Resposta vazia não enviada)')

    def get_response(self, user_input: str) -> str:
        lowered = user_input.lower()

        if lowered == '':
            return 'Bom, você está terrivelmente silencioso'
        elif 'karudê' in lowered:
            if 'bom dia' in lowered:
                return choice(['Bom diaaa! S2', 'Ohayō :D', 'Salvee ヾ(•ω•`)o'])
            elif 'você esta?' in lowered:
                return choice(['De boa na lagoa (￣o￣) . z Z', 'Estou escutando um Twice ❤', 'Só nos games ლ(╹◡╹ლ)'])
            elif 'tu esta?' in lowered:
                return choice(['Só pelo churras －O－', 'Os gurizes estão bem ;P', 'Só no chimas ( •̀ ω •́ )✧'])
            elif 'ouvindo' in lowered:
                return choice([
                    'Estou ouvindo Twice - Like OOH-AHH', 'Estou ouvindo Twice - CHEER UP', 'Estou ouvindo Twice - TT',
                    'Estou ouvindo Twice - Knock Knock', 'Estou ouvindo Twice - Signal', 'Estou ouvindo Twice - Likey',
                    'Estou ouvindo Twice - Heart Shaker', 'Estou ouvindo Twice - Brand New Girl', 'Estou ouvindo Twice - Candy Pop',
                    'Estou ouvindo Twice - What is Love?', 'Estou ouvindo Twice - Dance The Night Away', 'Estou ouvindo Twice - YES or YES',
                    'Estou ouvindo Twice - The Best Thing I Ever Did', 'Estou ouvindo Twice - Fancy (a melhor)',
                    'Estou ouvindo Twice - Breakthrough', 'Estou ouvindo Twice - Feel Special', 'Estou ouvindo Twice - Fake & True',
                    'Estou ouvindo Twice - More & More', 'Estou ouvindo System Of A Down - Toxicity', 'Estou ouvindo Slipknot - Psychosocial',
                    'Estou ouvindo Metallica - One', 'Estou ouvindo KoRn- Freak On a Leash', 'Estou ouvindo DJ Matt-D - Pandora',
                    'Estou ouvindo Foo Fighters - Everlong', 'Estou ouvindo Calypso - Entre Tapas e Beijos', 'Estou ouvindo Kyary Pamyu Pamyu - PONPONPON',
                    'Estou ouvindo BABYMETAL - Gimme chocolate!!', 'Estou ouvindo Gorillaz - 19-2000', 'Estou ouvindo Chico Buarque - Construção',
                    'Estou ouvindo Kyary Pamyu Pamyu - PONPONPON'
                ])
            elif 'está bem?' in lowered:
                return choice(['Estou tranquila :D', 'De buenas', 'Watashi wa genkidesu'])
            elif 'esta fazendo?' in lowered:
                return choice(['Estou programando <:actually:1263690743864758395>', 'Escutando Twice ❤❤❤', 'Passando raiva no vava'])
            elif 'oi' in lowered:
                return choice(['Chama! o((>ω< ))o', 'yippieeee! ヾ(≧▽≦*)o'])
            elif 'tudo bem?' in lowered:
                return choice(['De boa e tu?', 'Estou bem, mas trouxe os refris?', 'Bem, já fez o curso?'])
            elif 'tchau' in lowered:
                return choice(['Até ;)', 'Bye bye', 'Sayōnara'])
            elif 'gosta de valorant' in lowered:
                return choice(['Amo, mas odeio S2', 'A mãe é main Jet, sou melhor que o Aspas (○｀ 3′○)', 'Gosto, só não dos Noobs (╯‵□′)╯︵┻━┻'])
            elif 'academia' in lowered:
                return choice(['Credo ＞︿＜', 'Que isso?', 'Desconheço U_U'])
            elif 'trilha favorita' in lowered:
                return 'Não tenho uma trilha favorita, mas por algum motivo, gosto muito de python ;)'
            else:
                return choice([
                    'Não manjo o que tu falou ＞﹏＜, se tiver alguma duvida, sobre o que eu respondo: !Karude falas',
                    'Que bagulho doido é esse? （︶^︶）Se tem duvida, digite: !Karude falas',
                    'Cara, não ablo isso não (╬▔皿▔)╯, só digite: !Karude falas'
                ])

        return ''

async def setup(bot: commands.Bot):
    await bot.add_cog(Responses(bot))