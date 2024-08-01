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
        self.scores = {}

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
                        description="Parabéns! 🎉",
                        color=discord.Color.green()
                    )
                    self.scores[ctx.author.name] = self.scores.get(ctx.author.name, 0) + 1
                else:
                    embed = discord.Embed(
                        title="Incorreto!",
                        description=f"A resposta correta era: {answer}",
                        color=discord.Color.red()
                    )
                await ctx.send(embed=embed)

    @commands.command(name='ranking')
    async def ranking(self, ctx):
        if not self.scores:
            await ctx.send("Nenhuma pontuação registrada ainda.")
            return

        ranking = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        description = "\n".join([f"{i + 1}. {user} - {score} pontos" for i, (user, score) in enumerate(ranking)])
        embed = discord.Embed(
            title="Ranking de Trivia",
            description=description,
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(JogoQuiz(bot))
