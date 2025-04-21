from discord.ext import commands
import discord
import random
import asyncio
import sqlite3

DB_PATH = "trivia.db"  # Caminho do banco de dados

class JogoQuiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trivia_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    EMOJI_TO_CATEGORY = {
        '🐍': 'python',
        '☕': 'java',
        '🎨': 'marketing_design',
        '💼': 'gestao_vendas',
    }

    @commands.command(name='addpergunta')
    async def add_question(self, ctx, *, input_text: str):
        """Adicionar nova pergunta ao banco (ex: !addpergunta python | Qual a palavra-chave para função? | def)"""
        # Substitua com o ID real do cargo de professor
        ROLE_ID = 1100472796510957589

        if ROLE_ID not in [role.id for role in ctx.author.roles]:
            return await ctx.send("Você não tem permissão para adicionar perguntas.")

        try:
            category, question, answer = [x.strip() for x in input_text.split("|")]
        except ValueError:
            return await ctx.send("Formato inválido! Use: `!addpergunta categoria | pergunta | resposta`")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trivia_questions (category, question, answer) VALUES (?, ?, ?)", (category, question, answer))
        conn.commit()
        conn.close()

        await ctx.send(f"Pergunta adicionada com sucesso à categoria `{category}`! ✅")

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
            return

        category = self.EMOJI_TO_CATEGORY[str(reaction.emoji)]

        # Buscar pergunta aleatória da categoria
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM trivia_questions WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            await ctx.send("Categoria sem perguntas disponíveis.")
            return

        question, answer = result

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
            await ctx.send(embed=discord.Embed(
                title="Tempo esgotado!",
                description=f"A resposta correta era: {answer}",
                color=discord.Color.red()
            ))
        else:
            if msg.content.lower().strip() == answer.lower().strip():
                await ctx.send(embed=discord.Embed(
                    title="Correto!",
                    description="Parabéns! 🎉 Você ganhou 100 créditos!",
                    color=discord.Color.green()
                ))
                await self.update_balance(ctx.author.id, 100)
            else:
                await ctx.send(embed=discord.Embed(
                    title="Incorreto!",
                    description=f"A resposta correta era: {answer}",
                    color=discord.Color.red()
                ))

    async def update_balance(self, user_id, amount):
        """Atualizar saldo do usuário"""
        import json, os
        economy_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "economy_data.json")

        if not os.path.exists(economy_file):
            with open(economy_file, 'w') as f:
                json.dump({}, f)

        with open(economy_file, 'r') as f:
            economy_data = json.load(f)

        if str(user_id) not in economy_data:
            economy_data[str(user_id)] = {"balance": 0}

        economy_data[str(user_id)]["balance"] += amount

        with open(economy_file, 'w') as f:
            json.dump(economy_data, f)

# Setup do Cog
async def setup(bot):
    await bot.add_cog(JogoQuiz(bot))