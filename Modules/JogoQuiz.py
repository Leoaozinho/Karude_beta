from discord.ext import commands
import discord
import random
import asyncio
import os
import json


class JogoQuiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TRIVIA_QUESTIONS = self.load_questions()

    def load_questions(self):
        questions = {}
        questions_folder = 'Questions'
        for filename in os.listdir(questions_folder):
            if filename.endswith('.json'):
                category = filename.replace('.json', '')
                with open(os.path.join(questions_folder, filename), 'r', encoding='utf-8') as f:
                    questions[category] = json.load(f)
        return questions

    EMOJI_TO_CATEGORY = {
        '🐍': 'python',
        '☕': 'java',
        '🎨': 'marketing_design',
        '💼': 'gestao_vendas',
    }

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        # Criar embed para a mensagem inicial de seleção de categoria
        embed = discord.Embed(
            title="Escolha uma categoria para a trivia!",
            description=(
                "Reaja com um emoji para escolher uma categoria:\n"
                "🐍 - Python\n"
                "☕ - Java\n"
                "🎨 - Marketing e Design\n"
                "💼 - Gestão de Vendas"
            ),
            color=discord.Color.blue()
        )
        category_message = await ctx.send(embed=embed)

        # Adicionar reações para cada categoria
        for emoji in self.EMOJI_TO_CATEGORY.keys():
            await category_message.add_reaction(emoji)

        def check_reaction(reaction, user):
            return (
                    user == ctx.author and
                    str(reaction.emoji) in self.EMOJI_TO_CATEGORY and
                    reaction.message.id == category_message.id
            )

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado! Por favor, tente novamente.")
        else:
            category = self.EMOJI_TO_CATEGORY[str(reaction.emoji)]
            questions = self.TRIVIA_QUESTIONS.get(category, [])

            if not questions:
                await ctx.send("Categoria não encontrada ou sem perguntas.")
                return

            question, answer = random.choice(questions)

            # Criar embed para a pergunta
            embed = discord.Embed(
                title=f"Categoria: {category}",
                description=f"Pergunta: {question}",
                color=discord.Color.green()
            )
            embed.set_footer(text="Você tem 15 segundos para responder.")
            await ctx.send(embed=embed)

            def check_answer(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check_answer)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Tempo esgotado!",
                    description=f"A resposta correta era: {answer}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                if msg.content.lower() == answer.lower():
                    embed = discord.Embed(
                        title="Correto!",
                        description="Parabéns! 🎉 Você ganhou 100 créditos!",
                        color=discord.Color.green()
                    )
                    await self.update_balance(ctx.author.id, 100)  # Atualizar saldo com 100 créditos
                else:
                    embed = discord.Embed(
                        title="Incorreto!",
                        description=f"A resposta correta era: {answer}",
                        color=discord.Color.red()
                    )
                await ctx.send(embed=embed)

    async def update_balance(self, user_id, amount):
        """Função para atualizar o saldo do usuário. Deve ser integrada ao sistema de economia existente."""
        with open('economy_data.json', 'r') as f:
            economy_data = json.load(f)

        if str(user_id) not in economy_data:
            economy_data[str(user_id)] = {"balance": 0}

        economy_data[str(user_id)]["balance"] += amount

        with open('economy_data.json', 'w') as f:
            json.dump(economy_data, f)


# Para adicionar o Cog ao bot
async def setup(bot):
    await bot.add_cog(JogoQuiz(bot))
