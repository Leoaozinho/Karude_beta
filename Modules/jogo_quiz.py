from discord.ext import commands
import random
import asyncio
import discord

# Perguntas e respostas
TRIVIA_QUESTIONS = {
    'Python': [
        ("Qual é a saída de print(2 ** 3)?", "8"),
        ("Como se define uma função em Python?", "def"),
        ("Qual é a saída de print(3 + 4 * 2)?", "11"),
        ("Como se cria uma lista em Python?", "Usando colchetes, por exemplo: []"),
        ("O que é PEP 8?", "Guia de estilo para escrever código Python"),
        ("Como você pode adicionar um elemento a uma lista em Python?", "Usando o método append(), por exemplo: "
                                                                        "lista.append(item)"),
        ("O que significa self em um método de classe em Python?", "Referência à instância da própria classe"),
        ("Qual é o método para remover espaços em branco de uma string?", "strip()"),
        ("Como você pode inverter uma string em Python?", "Usando slicing, por exemplo: string[::-1]"),
        ("O que é um dicionário em Python?", "Uma coleção de pares chave-valor"),
        ("Como você pode remover um item de um dicionário?", "Usando o método pop() ou a palavra-chave del"),
        ("Qual é a diferença entre list e tuple?", "Listas são mutáveis, enquanto tuplas são imutáveis"),
        ("O que faz a função len()?", "Retorna o número de itens em um objeto"),
        ("O que é uma lambda em Python?", "Uma função anônima de uma única linha"),
        ("O que é uma list comprehension?", "Uma maneira concisa de criar listas"),
        ("Como você pode importar uma biblioteca em Python?", "Usando a palavra-chave import"),
        ("O que é o Pandas?", "Uma biblioteca para análise de dados"),
        ("O que faz o método groupby() em Pandas?", "Agrupa os dados por uma ou mais chaves"),
        ("Qual é a diferença entre Series e DataFrame no Pandas?", "Uma Series é uma coluna única, enquanto um "
                                                                   "DataFrame é uma tabela de dados"),
        ("Como você pode ler um arquivo CSV usando Pandas?", "Usando a função pd.read_csv()"),
        ("O que é NumPy?", "Uma biblioteca para computação científica e array de n-dimensões"),
        ("Como você cria um array NumPy?", "Usando np.array()"),
        ("O que é o matplotlib?", "Uma biblioteca para visualização de dados"),
        ("Como você pode criar um gráfico de linha em matplotlib?", "Usando plt.plot()"),
        ("O que é scikit-learn?", "Uma biblioteca para machine learning em Python"),
        ("Qual é a função de train_test_split() em scikit-learn?", "Divide os dados em conjuntos de treino e teste"),
        ("O que é uma Regressão Linear?", "Uma técnica de modelagem preditiva para dados contínuos"),
        ("O que é overfitting?", "Quando um modelo se ajusta muito bem aos dados de treino, mas falha em generalizar "
                                 "para novos dados"),
        ("Como você pode evitar overfitting?", "Usando regularização, "
                                               "aumento de dados ou técnicas de validação cruzada"),
        ("O que é uma Redes Neurais?", "Um modelo de machine learning inspirado na estrutura do cérebro"),
        ("O que é um Perceptron?", "A unidade básica de uma rede neural"),
        ("O que é uma Função de Ativação?", "Uma função que decide se um neurônio deve ser ativado ou não"),
        ("O que é Deep Learning?", "Um subcampo do machine learning com redes neurais profundas"),
        ("O que é uma Convolutional Neural Network (CNN)?", "Uma rede neural usada para processar dados estruturados "
                                                            "em grade, como imagens"),
        ("O que é uma Recurrent Neural Network (RNN)?", "Uma rede neural projetada para processar sequências de dados"),
        ("O que é TensorFlow?", "Uma biblioteca de machine learning desenvolvida pelo Google"),
        ("Qual é o propósito da Keras?", "Uma API de alto nível para construir e treinar modelos de redes neurais"),
        ("O que é overfitting em modelos de machine learning?", "Quando o modelo se ajusta muito bem aos dados de "
                                                                "treino e não generaliza para novos dados"),
        ("Como você pode avaliar a performance de um modelo de classificação?", "Usando métricas como accuracy, "
                                                                                "precision, recall e F1-score"),
        ("O que é cross-validation?", "Uma técnica para avaliar a capacidade de generalização de um modelo"),
        ("O que é um Random Forest?", "Um conjunto de árvores de decisão usado para classificação e regressão"),
        ("O que é o K-means?", "Um algoritmo de clustering não supervisionado"),
        ("Como você pode visualizar um conjunto de dados usando seaborn?", "Usando funções como sns.scatterplot(), "
                                                                           "sns.histplot(), etc."),
        ("O que é PCA em machine learning?", "Análise de Componentes Principais, uma técnica de redução de "
                                             "dimensionalidade"),
        ("Como você pode lidar com dados faltantes em um DataFrame Pandas?", "Usando dropna() para remover ou fillna("
                                                                             ") para substituir valores faltantes"),
        ("O que é Gradient Descent?", "Um algoritmo para encontrar o mínimo de uma função"),
        ("O que é um Hyperparameter em machine learning?", "Parâmetros de um modelo que são ajustados antes do "
                                                           "processo de aprendizado"),
        ("Como você pode salvar um modelo treinado em scikit-learn?", "Usando joblib ou pickle"),
        ("O que é Exploratory Data Analysis (EDA)?", "O processo de analisar conjuntos de dados para resumir suas "
                                                     "características principais"),
        ("O que é um Outlier?", "Um dado que se desvia significativamente dos outros dados"),
        ("O que é Natural Language Processing (NLP)?", "Um campo da inteligência artificial focado na interação entre "
                                                       "computadores e linguagem humana")
    ],
    'Java': [
        ("Qual é a saída de System.out.println(2 + 3 * 4);?", "14"),
        ("Como você declara uma variável em Java?", "Usando o tipo e o nome da variável, por exemplo: int x;"),
        ("O que é uma classe em Java?", "Uma estrutura de código que define as propriedades e comportamentos de um "
                                        "objeto"),
        ("Como você cria um objeto em Java?", "Usando a palavra-chave new, por exemplo: new MyClass();"),
        ("Qual é a diferença entre == e equals() em Java?", "== compara referências, equals() compara valores"),
        ("O que é uma interface em Java?", "Um contrato que uma classe pode implementar"),
        ("Como você define uma constante em Java?", "Usando a palavra-chave final"),
        ("O que é um construtor em Java?", "Um método especial usado para inicializar objetos"),
        ("Qual é a saída de System.out.println(\"Hello\" + \"World\");?", "HelloWorld"),
        ("Como você define um método em Java?", "Com um modificador de acesso, tipo de retorno, nome e parâmetros, "
                                                "por exemplo: public void myMethod()"),
        ("O que é um método estático?", "Um método que pertence à classe, e não a uma instância"),
        ("Qual é a palavra-chave para herança em Java?", "extends"),
        ("O que é encapsulamento?", "A prática de restringir o acesso a certos componentes de um objeto"),
        ("O que é polimorfismo em Java?", "A capacidade de uma variável, função ou objeto de tomar várias formas"),
        ("O que é uma exceção em Java?", "Um evento que interrompe o fluxo normal de um programa"),
        ("Como você lida com exceções em Java?", "Usando blocos try-catch"),
        ("O que é uma classe abstrata?", "Uma classe que não pode ser instanciada e pode ter métodos abstratos"),
        ("O que é uma string imutável?", "Uma string cujo valor não pode ser alterado após a criação"),
        ("Como você converte uma string em um número em Java?", "Usando métodos como Integer.parseInt() ou "
                                                                "Double.parseDouble()"),
        ("O que é o public em um método ou classe?", "Um modificador de acesso que permite que o método ou classe "
                                                     "seja acessível de qualquer lugar"),
        ("Qual é a diferença entre ArrayList e LinkedList?", "ArrayList é baseado em um array dinâmico, enquanto "
                                                             "LinkedList é baseado em uma lista duplamente encadeada"),
        ("O que é uma HashMap?",
         "Uma estrutura de dados que armazena pares chave-valor e não permite chaves duplicadas"),
        ("O que é um HashSet?", "Uma coleção que não permite elementos duplicados e é baseada em uma tabela hash"),
        ("Qual é a diferença entre uma lista e um conjunto em Java?", "Uma lista permite elementos duplicados e é "
                                                                      "ordenada, enquanto um conjunto não permite "
                                                                      "duplicatas e não garante ordem"),
        ("O que é uma enumeração?", "Um tipo especial de classe que representa um grupo de constantes (variáveis "
                                    "imutáveis)"),
        ("Como você faz um loop for em Java?", "Usando a sintaxe for (inicialização; condição; atualização) { // "
                                               "bloco de código }"),
        ("O que é JVM?", "Java Virtual Machine, um motor que executa bytecode Java"),
        ("O que é JRE?", "Java Runtime Environment, um conjunto de ferramentas para executar aplicações Java"),
        ("O que é JDK?", "Java Development Kit, um kit de ferramentas para desenvolver aplicações Java"),
        ("Qual é o propósito do método main() em Java?", "É o ponto de entrada de um aplicativo Java"),
        ("O que é uma classe interna?", "Uma classe definida dentro de outra classe"),
        ("O que são genéricos em Java?", "Uma maneira de definir classes, interfaces e métodos com parâmetros de tipo"),
        ("Como você realiza a serialização em Java?", "Usando a interface Serializable"),
        ("O que é a palavra-chave final?", "Indica que um valor não pode ser modificado ou um método não pode ser "
                                           "sobreposto"),
        ("O que é sobrecarga de método?", "Definir vários métodos com o mesmo nome mas diferentes parâmetros"),
        ("O que é sobreposição de método?", "Definir um método em uma subclasse com a mesma assinatura de um método "
                                            "na superclasse"),
        ("O que é o operador instanceof?", "Verifica se um objeto é uma instância de uma classe específica"),
        ("O que é um pacote em Java?", "Um agrupamento de classes e interfaces relacionadas"),
        ("Como você importa uma classe de outro pacote?", "Usando a palavra-chave import seguida do nome completo do "
                                                          "pacote e classe"),
        ("O que é multithreading?", "A capacidade de um programa executar várias threads simultaneamente"),
        ("O que é o método sleep()?", "Faz a thread atual esperar por um determinado período de tempo"),
        ("Qual é a diferença entre wait() e sleep()?", "wait() libera o lock no objeto e espera até ser notificado, "
                                                       "sleep() apenas pausa a thread"),
        ("O que é uma synchronized em Java?", "Um bloco de código que só pode ser acessado por uma thread por vez"),
        ("O que é o Garbage Collection?", "O processo de liberar memória ocupada por objetos que não são mais usados"),
        ("O que é o transient em Java?", "Indica que um campo não deve ser serializado"),
        ("O que é um bloco try-catch?", "Usado para capturar e tratar exceções"),
        ("O que é um interface functional?", "Uma interface com exatamente um método abstrato"),
        ("O que é o stream em Java 8?", "Uma sequência de elementos suportando operações de agregação e filtragem"),
        ("Como você trabalha com arquivos em Java?", "Usando classes como FileReader, FileWriter, BufferedReader, "
                                                     "BufferedWriter"),
        ("O que é a Optional em Java?", "Uma classe usada para representar um valor que pode ou não estar presente")
    ],
    'Marketing e Design': [
        ("O que significa SEO?", "Search Engine Optimization"),
        ("O que é uma persona de marketing?", "Uma representação semi-fictícia do cliente ideal"),
        ("O que é uma call to action (CTA)?", "Uma instrução para o público-alvo realizar uma ação imediata"),
        ("Qual é o propósito de um logotipo?", "Identificar uma marca ou empresa"),
        ("O que é marketing de conteúdo?", "Uma estratégia focada na criação e distribuição de conteúdo valioso para "
                                           "atrair e engajar um público-alvo"),
        ("O que é uma landing page?", "Uma página da web dedicada a uma oferta específica e projetada para converter "
                                      "visitantes em leads ou clientes"),
        ("Qual é a diferença entre branding e marketing?", "Branding é a construção da identidade de uma marca, "
                                                           "enquanto marketing é a promoção e venda de produtos ou "
                                                           "serviços"),
        ("O que é uma campanha de marketing?", "Um conjunto coordenado de ações de marketing para promover um "
                                               "produto, serviço ou ideia"),
        ("O que é uma newsletter?", "Uma publicação digital ou impressa enviada regularmente aos assinantes para "
                                    "informá-los sobre novidades e conteúdos"),
        ("O que é remarketing?", "Uma estratégia de marketing que visa alcançar novamente usuários que já interagiram "
                                 "com uma marca ou site"),
        ("O que é PPC (Pay-Per-Click)?", "Um modelo de publicidade online onde os anunciantes pagam por cada clique "
                                         "em seus anúncios"),
        ("O que é um funil de vendas?", "Um modelo que ilustra o caminho que os consumidores percorrem desde o "
                                        "conhecimento do produto até a compra"),
        ("O que é a taxa de conversão?", "A porcentagem de visitantes de um site ou campanha que realizam uma ação "
                                         "desejada, como fazer uma compra"),
        ("O que é um layout responsivo?", "Um design de site que se adapta automaticamente a diferentes tamanhos de "
                                          "tela e dispositivos"),
        ("O que é UX (User Experience)?", "A experiência geral do usuário ao interagir com um produto ou serviço"),
        ("O que é UI (User Interface)?", "O design e os elementos visuais com os quais o usuário interage em um "
                                         "produto ou sistema"),
        ("O que é uma paleta de cores?", "Um conjunto específico de cores escolhido para uso em um projeto de design"),
        ("O que é tipografia?", "O estilo, arranjo e aparência do texto em um design"),
        ("O que é um wireframe?", "Um esboço básico ou guia visual de uma página da web ou aplicativo"),
        ("O que é um mockup?", "Um modelo visual de um design, usado para apresentar a aparência final"),
        ("O que é uma análise SWOT?", "Uma técnica de planejamento estratégico que identifica pontos fortes, fracos, "
                                      "oportunidades e ameaças"),
        ("O que é marketing de influência?", "Uma forma de marketing que se concentra em usar líderes de opinião para "
                                             "promover uma marca"),
        ("O que é um anúncio patrocinado?", "Um anúncio pago para promover conteúdo em plataformas de mídia social ou "
                                            "sites"),
        ("O que é marketing viral?", "Uma estratégia de marketing que incentiva as pessoas a compartilhar conteúdo "
                                     "com sua rede para aumentar a exposição"),
        ("O que é o Google Analytics?", "Uma ferramenta gratuita do Google que coleta e analisa dados sobre o tráfego "
                                        "de sites"),
        ("O que é uma métrica de engajamento?", "Dados que medem o nível de interação dos usuários com o conteúdo, "
                                                "como curtidas, compartilhamentos e comentários"),
        ("O que é um estudo de caso?", "Uma análise detalhada de um projeto ou campanha bem-sucedida para mostrar "
                                       "resultados e estratégias"),
        ("O que é um storyboard?", "Uma série de quadros ou esboços que ilustram a sequência de cenas em um vídeo ou "
                                   "animação"),
        ("O que é um teste A/B?", "Um experimento que compara duas versões de um conteúdo para ver qual tem melhor "
                                  "desempenho"),
        ("O que é uma estratégia de branding?", "O plano de longo prazo para o desenvolvimento de uma marca e a "
                                                "construção de seu valor"),
        ("O que é um logo?", "Um símbolo ou design que representa uma empresa ou marca"),
        ("O que é copywriting?", "A escrita de textos persuasivos para marketing e publicidade"),
        ("O que é uma identidade visual?", "Os elementos visuais que representam uma marca, como logotipo, cores e "
                                           "tipografia"),
        ("O que é o marketing de busca (SEM)?", "Marketing digital que envolve a promoção de sites aumentando sua "
                                                "visibilidade nos resultados de busca"),
        ("O que é uma segmentação de mercado?", "A divisão de um mercado em grupos de consumidores com "
                                                "características ou necessidades semelhantes"),
        ("O que é uma proposta de valor?", "A declaração de benefícios exclusivos que uma empresa oferece aos seus "
                                           "clientes"),
        ("O que é marketing de afiliados?", "Um modelo de marketing em que uma empresa paga comissões a afiliados por "
                                            "vendas geradas por sua indicação"),
        ("O que é um briefing de design?",
         "Um documento que descreve os requisitos e objetivos de um projeto de design"),
        ("O que é a saturação de cor?", "A intensidade ou pureza de uma cor"),
        ("O que é a regra dos terços?", "Uma diretriz de composição visual que divide uma imagem em três partes para "
                                        "criar equilíbrio"),
        ("O que é uma marca d'água?", "Uma imagem ou texto semi-transparente usado para proteger direitos autorais ou "
                                      "marcar propriedade"),
        ("O que é um infográfico?", "Uma representação visual de informações ou dados"),
        ("O que é o conceito de 'pain point' em marketing?", "Um problema ou necessidade específica que os clientes "
                                                             "enfrentam e que uma empresa pode resolver"),
        ("O que é a jornada do cliente?", "O processo completo pelo qual um cliente passa ao interagir com uma "
                                          "empresa, desde o conhecimento até a pós-compra"),
        ("O que é um lead?", "Um potencial cliente que demonstrou interesse em produtos ou serviços de uma empresa"),
        ("O que é o marketing de guerrilha?", "Táticas de marketing não convencionais e de baixo custo para atrair a "
                                              "atenção do público"),
        ("O que é o marketing de relacionamento?", "Estratégias para construir e manter relacionamentos de longo "
                                                   "prazo com os clientes"),
        ("O que é o conceito de 'top of mind'?", "A primeira marca ou produto que vem à mente de um consumidor em uma "
                                                 "categoria"),
        ("O que é uma rede social de nicho?", "Uma plataforma de mídia social voltada para um interesse ou grupo "
                                              "específico"),
        ("O que é uma análise de concorrência?",
         "A avaliação dos pontos fortes e fracos dos concorrentes em um mercado"),
    ],
    'Gestão de Vendas': [
        ("O que é CRM?", "Customer Relationship Management"),
        ("O que é prospecção de clientes?", "A busca e identificação de potenciais clientes"),
        ("O que é um lead?", "Um potencial cliente que demonstrou interesse em produtos ou serviços"),
        ("O que é a qualificação de leads?",
         "O processo de avaliar se um lead tem potencial para se tornar um cliente"),
        ("O que é follow-up?", "O acompanhamento de um prospecto após uma interação inicial"),
        ("O que é funil de vendas?", "Um modelo que descreve as etapas que um cliente passa desde o conhecimento até "
                                     "a compra"),
        ("O que é uma proposta de valor?", "Uma declaração de benefícios que uma empresa oferece aos clientes"),
        ("O que é a técnica de vendas SPIN?", "Uma técnica que usa perguntas para identificar Situações, Problemas, "
                                              "Implicações e Necessidades de soluções"),
        ("O que é uma objeção de venda?", "Uma razão ou preocupação levantada por um cliente para não fazer a compra"),
        ("O que é uma pipeline de vendas?", "Uma visualização das etapas que um lead passa até se tornar um cliente"),
        ("O que é venda consultiva?", "Uma abordagem de vendas que se concentra em entender as necessidades do "
                                      "cliente e oferecer soluções personalizadas"),
        ("O que é upselling?", "A técnica de oferecer ao cliente uma versão mais cara do produto ou serviço que ele "
                               "está comprando"),
        ("O que é cross-selling?", "A técnica de vender produtos ou serviços adicionais ao cliente"),
        ("O que é churn rate?", "A taxa de clientes que deixam de usar o produto ou serviço de uma empresa"),
        ("O que é ticket médio?", "O valor médio gasto por cliente em uma compra"),
        ("O que é ROI (Retorno sobre Investimento)?", "Uma medida de rentabilidade que calcula o retorno gerado sobre "
                                                      "o investimento"),
        ("O que é B2B (Business to Business)?", "Transações comerciais entre empresas"),
        ("O que é B2C (Business to Consumer)?", "Transações comerciais entre empresas e consumidores finais"),
        ("O que é uma call to action?", "Uma instrução para o público realizar uma ação específica, como fazer uma "
                                        "compra"),
        ("O que é cold call?", "Uma chamada telefônica não solicitada a um potencial cliente"),
        ("O que é uma demonstração de produto?", "Uma apresentação prática de como um produto ou serviço funciona"),
        ("O que é um pitch de vendas?", "Uma apresentação breve e persuasiva sobre um produto ou serviço"),
        ("O que é uma proposta comercial?", "Um documento formal que apresenta uma oferta de venda para um potencial "
                                            "cliente"),
        ("O que é a técnica de fechamento?", "Métodos e estratégias usados para convencer o cliente a finalizar a "
                                             "compra"),
        ("O que é a abordagem AIDA (Atenção, Interesse, Desejo, Ação)?", "Um modelo de comunicação de marketing que "
                                                                         "descreve as etapas que uma mensagem deve "
                                                                         "seguir para levar o consumidor à ação"),
        ("O que é segmentação de mercado?", "A divisão de um mercado em grupos de consumidores com características ou "
                                            "necessidades semelhantes"),
        ("O que é uma buyer persona?", "Uma representação semi-fictícia do cliente ideal baseada em dados reais"),
        ("O que é NPS (Net Promoter Score)?", "Uma métrica que avalia a lealdade dos clientes com base na "
                                              "probabilidade de recomendarem a empresa"),
        ("O que é uma taxa de conversão?", "A porcentagem de visitantes de um site ou campanha que realizam uma ação "
                                           "desejada"),
        ("O que é um ciclo de vendas?", "O período desde o primeiro contato com o cliente até a conclusão da venda"),
        ("O que é a gestão de relacionamento com o cliente?", "Estratégias e práticas usadas para gerenciar e "
                                                              "analisar as interações com clientes"),
        ("O que é a técnica de ancoragem?", "Uma técnica de negociação onde um preço inicial é estabelecido para "
                                            "influenciar a percepção de valor do cliente"),
        ("O que é uma estratégia de precificação?", "Um plano para determinar o preço de um produto ou serviço"),
        ("O que é uma análise SWOT em vendas?", "Uma análise que avalia os pontos fortes, fracos, oportunidades e "
                                                "ameaças em vendas"),
        ("O que é uma venda de ciclo curto?", "Uma venda que é concluída rapidamente, com poucas interações"),
        ("O que é uma venda de ciclo longo?", "Uma venda que leva muito tempo para ser concluída e envolve várias "
                                              "interações"),
        ("O que é uma análise de concorrência?",
         "A avaliação dos pontos fortes e fracos dos concorrentes em um mercado"),
        ("O que é uma comissão de vendas?", "Uma remuneração adicional paga aos vendedores com base nas vendas que "
                                            "eles geram"),
        ("O que é um quota de vendas?", "Uma meta de vendas estabelecida para um vendedor ou equipe de vendas"),
        ("O que é uma taxa de sucesso?", "A proporção de vendas realizadas em relação às oportunidades de venda"),
        ("O que é a técnica de fechamento alternativo?", "Uma técnica onde o vendedor apresenta ao cliente duas "
                                                         "opções, ambas levando à compra"),
        ("O que é o método de vendas Challenger?", "Um modelo de vendas que desafia os clientes a pensar de maneira "
                                                   "diferente sobre suas necessidades"),
        ("O que é a técnica de vendas Sandler?", "Uma metodologia de vendas que se concentra em construir uma relação "
                                                 "de confiança com o cliente"),
        ("O que é o método de vendas Miller Heiman?", "Uma abordagem de vendas que se concentra em entender e atender "
                                                      "às necessidades complexas de grandes contas"),
        ("O que é uma reunião de kickoff de vendas?", "Uma reunião inicial para alinhar a equipe de vendas com os "
                                                      "objetivos e estratégias de uma campanha"),
        ("O que é uma análise de pipeline?",
         "A avaliação do progresso dos leads através das etapas do funil de vendas"),
        ]
}


# Comando de trivia
@commands.command(name='trivia')
async def start_trivia(ctx):
    embed = discord.Embed(title="Quiz de Conhecimento", description="Selecione uma categoria:",
                          color=discord.Color.blue())
    embed.add_field(name="1", value="Python", inline=False)
    embed.add_field(name="2", value="Java", inline=False)
    embed.add_field(name="3", value="Marketing e Design", inline=False)
    embed.add_field(name="4", value="Gestão de Vendas", inline=False)
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.content.isdigit()

    try:
        response = await ctx.bot.wait_for('message', check=check, timeout=30.0)
        category_num = int(response.content)

        categories = list(TRIVIA_QUESTIONS.keys())
        if 1 <= category_num <= len(categories):
            category = categories[category_num - 1]
            question, answer = random.choice(TRIVIA_QUESTIONS[category])
            await ctx.send(f"Categoria: {category}\n{question}")

            def answer_check(m):
                return m.author == ctx.author

            try:
                user_answer = await ctx.bot.wait_for('message', check=answer_check, timeout=30.0)
                if user_answer.content.lower() == answer.lower():
                    await ctx.send("Correto!")
                else:
                    await ctx.send(f"Errou! Não foi dessa vez. Mas a resposta certa era: {answer}")
            except asyncio.TimeoutError:
                await ctx.send("Você ficou afk por muito tempo e levou disconnect!")
        else:
            await ctx.send("Número de categoria inválido.")
    except asyncio.TimeoutError:
        await ctx.send("Você ficou afk e não escolheu a categoria. Timeout pra ti!")


# Função setup para registrar o comando
def setup(bot):
    bot.add_command(start_trivia)
