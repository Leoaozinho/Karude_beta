> [!NOTE]
> ## Nosso ambiente de desenvolvimento daora :shipit: :trollface:

> **criar ambiente de desenvolvimento python**
> ~~~bash
> python3 -m venv .venv
> ~~~

> **acessar o ambiente de desenvolvimento**
> ~~~bash
> source .venv/bin/activate
> ~~~

> **sair do ambientede de desenvolvimento**
> ~~~bash
> deactivate
> ~~~

> **instalar bibliotecas do projeto**
> ~~~bash
> pip3 install -r requirements.txt
> ~~~

> **incluir bibliotecas no projeto**
> ~~~bash
> pip3 freeze karude > requirements.txt
> ~~~

## **Como posso nomear os commit?**
> Assim:

> "Mxxxx - Descrição do commit"

> ~~~text
> M -> Modificação
> x -> numero da modificação, será sempre crescente
> Confira o repositório antes de fazer o push. S2
> Logo o Brunitux automatiza isso, senta lá Jéssica
> ~~~


## **Criar banco de dados caso não exista alguma tabela**
> ~~~bash
> python criar-db.py
> ~~~

## **Ler o conteúdo de todo o banco de dados do arquivo .db**
> ~~~bash
> python ler-tabela.py
> ~~~

> Escreva as criações das tabelas manualmente no arquivo "criar-db.py"
> para que não haja criação recursiva de tabelas em cada comando,
> assim cada tabela só é criada quando necessário, evitando consultas
> extras ao banco de dados.
