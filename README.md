> [!TIP]
> Dicas básicas para um ambiente de desenvolvimento daora ;D

# criar ambiente de desenvolvimento python
~~~bash
python3 -m venv karude
~~~

# acessar o ambiente de desenvolvimento
~~~bash
source karude/bin/activate
~~~

# sair do ambientede de desenvolvimento
~~~bash
deactivate
~~~

# instalar bibliotecas do projeto
~~~bash
pip3 install -r requirements.txt
~~~

# incluir bibliotecas no projeto
~~~bash
pip3 freeze karude > requirements.txt
~~~