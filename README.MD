Gerador de Receitas
Visão Geral do Projeto
Este é um projeto de um Gerador de Receitas construído com o framework web Django. A aplicação permite aos usuários criar e gerenciar suas próprias receitas, utilizando uma API externa para busca e tradução de informações detalhadas. O projeto foi desenvolvido com uma arquitetura modular, seguindo as melhores práticas do Django, e inclui funcionalidades robustas como um sistema de autenticação de usuário, gestão de perfis, um painel de moderação para receitas e uma interface de usuário completa e responsiva.

Tecnologias Utilizadas
O projeto foi desenvolvido com as seguintes tecnologias e bibliotecas:

Linguagem: Python

Framework Web: Django (versão 5.2.4)

Banco de Dados: SQLite (padrão do Django para desenvolvimento)

Estilização e Formulários:

Django Crispy Forms

Django Widget Tweaks

Outras Bibliotecas:

python-dotenv: Para gerenciar variáveis de ambiente de forma segura.

Pillow (PIL): Para redimensionar imagens de perfil.

rest_framework: Para a serialização de dados, indicando o uso de APIs.

googletrans: Para tradução de textos, como nomes de receitas e ingredientes.

django-cachalot: Para otimizar consultas ao banco de dados usando cache.

Bootstrap 5 e Font Awesome: Utilizados para estilização e ícones na interface do usuário.

Funcionalidades Principais
Autenticação de Usuário: Sistema completo de login, logout, registro e redefinição de senha com templates dedicados e estilizados.

Gestão de Perfil: Os usuários podem visualizar e editar suas informações de perfil, incluindo o upload de uma foto que é redimensionada automaticamente. Também é possível alterar a senha e ver uma lista das receitas enviadas.

Busca e Visualização de Receitas: O usuário pode buscar receitas por ingredientes e visualizar detalhes completos, incluindo uma lista de ingredientes e modo de preparo. Os resultados da busca são paginados.

Receitas Favoritas: Os usuários autenticados podem adicionar receitas à sua lista de favoritos, que fica disponível em uma página específica.

Avaliações e Comentários: É possível avaliar e comentar as receitas, com o ranking das mais bem avaliadas sendo exibido na página inicial.

Sistema de Moderação: Um painel exclusivo para superusuários permite a moderação de receitas enviadas por outros usuários, com status de aprovado ou pendente.

Página Inicial Dinâmica: A homepage exibe um ranking das receitas mais bem avaliadas para destacar o conteúdo popular da plataforma.

Como Instalar e Rodar o Projeto
Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

Pré-requisitos
Certifique-se de ter o seguinte software instalado:

Python (versão 3.8 ou superior)

pip (gerenciador de pacotes do Python)

Git (opcional, para clonar o repositório)

Instalação
Clone o repositório:

Bash

git clone https://github.com/seu-usuario/gerador-receitas.git
cd gerador-receitas
(Substitua o link pelo endereço do seu repositório no GitHub)

Crie e ative um ambiente virtual:
É uma boa prática isolar as dependências do projeto.

Bash

python -m venv venv
Windows:

Bash

venv\Scripts\activate
macOS e Linux:

Bash

source venv/bin/activate
Instale as dependências:
Crie o arquivo requirements.txt com o comando pip freeze > requirements.txt e instale as dependências:

Bash

pip install -r requirements.txt
Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto e adicione suas chaves secretas e configurações. Exemplo:

Ini, TOML

DJANGO_SECRET_KEY='sua-chave-secreta-aqui'
DJANGO_DEBUG='True'
EMAIL_HOST_USER='seu-email@gmail.com'
EMAIL_HOST_PASSWORD='sua-senha-de-app-do-google'
Execute as migrações do banco de dados:

Bash

python manage.py migrate
Crie um superusuário (opcional, para acessar o painel de admin e moderação):

Bash

python manage.py createsuperuser
Siga as instruções para criar seu usuário e senha.

Como Rodar o Projeto
Após a instalação, inicie o servidor de desenvolvimento do Django com o seguinte comando:

Bash

python manage.py runserver
O projeto estará disponível em http://127.0.0.1:8000.