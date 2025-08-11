# Gerador de Receitas





[](https://www.python.org/)

[](https://www.djangoproject.com/)

[](https://opensource.org/licenses/MIT)



#Construído com ❤️ por Henrique Castro



*Uma plataforma completa para buscar, traduzir e gerenciar receitas, usando o poder do Django e APIs externas.*





-----



## 📖 Tabela de Conteúdos



  * [💡 Sobre o Projeto](https://www.google.com/search?q=%23-sobre-o-projeto)

  * [✨ Funcionalidades](https://www.google.com/search?q=%23-funcionalidades)

  * [🚀 Tecnologias Utilizadas](https://www.google.com/search?q=%23-tecnologias-utilizadas)

  * [📸 Screenshots](https://www.google.com/search?q=%23-screenshots)

  * [🛠️ Como Rodar o Projeto](https://www.google.com/search?q=%23-como-rodar-o-projeto)

  * [📝 Licença](https://www.google.com/search?q=%23-licen%C3%A7a)

  * [🤝 Contribuições](https://www.google.com/search?q=%23-contribui%C3%A7%C3%B5es)



-----



## 💡 Sobre o Projeto



O **Gerador de Receitas** é uma aplicação web robusta, desenvolvida com o framework **Django**, projetada para simplificar a busca e a organização de receitas. A plataforma se destaca por sua capacidade de integrar-se com a API externa **TheMealDB** para pesquisar receitas e traduzir o conteúdo dinamicamente para o português.



O objetivo do projeto é oferecer uma experiência completa ao usuário, desde a navegação em um vasto catálogo de receitas até a criação e gestão de seu próprio conteúdo e perfil.



## ✨ Funcionalidades



| Funcionalidade                     | Descrição                                                                            |

| :--------------------------------- | :----------------------------------------------------------------------------------- |

| **Autenticação Completa** | Registro, login, logout e redefinição de senha com templates personalizados.           |

| **Gerenciamento de Perfil** | Edição de informações e upload de foto de perfil com redimensionamento automático.      |

| **Busca Dinâmica** | Pesquisa de receitas por ingredientes com resultados paginados.                        |

| **Moderação de Conteúdo** | Painel de administrador para aprovar/rejeitar receitas enviadas pelos usuários.      |

| **Ranking de Receitas** | A página inicial exibe as receitas mais bem avaliadas pelos usuários.                 |

| **Favoritos e Avaliações** | Os usuários podem salvar receitas favoritas e deixar avaliações e comentários.          |



## 🚀 Tecnologias Utilizadas



A seguir estão as principais tecnologias e bibliotecas utilizadas no desenvolvimento do projeto:



| Categoria | Tecnologia                                                                                             |

| :-------- | :----------------------------------------------------------------------------------------------------- |

| **Backend** |     |

| **Frontend** |   |

| **Integrações** |    |



## 📸 Screenshots



Aqui estão algumas capturas de tela da aplicação em funcionamento:



### Página Inicial com Ranking de Receitas



> *A imagem acima é um placeholder. Substitua o link pela URL da sua imagem (por exemplo, do Imgur ou do seu próprio repositório).*



### Perfil do Usuário



> *Dica: Use `![Descrição da imagem](URL_da_imagem)` para adicionar suas próprias imagens.*



## 🛠️ Como Rodar o Projeto



Siga os passos abaixo para ter uma cópia do projeto em execução na sua máquina.



### Pré-requisitos



Certifique-se de ter o seguinte software instalado:



  * [Python](https://www.python.org/downloads/) (versão 3.8+)

  * [pip](https://pip.pypa.io/en/stable/installation/) (gerenciador de pacotes do Python)

  * [Git](https://git-scm.com/downloads) (para clonar o repositório)



### Instalação



1.  **Clone o repositório:**

    ```bash

    git clone https://github.com/seu-usuario/gerador-receitas.git

    cd gerador-receitas

    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash

    python -m venv venv

    source venv/bin/activate  # Para macOS e Linux

    # venv\Scripts\activate   # Para Windows

    ```

3.  **Instale as dependências:**

    ```bash

    pip install -r requirements.txt

    ```

4.  **Configure as variáveis de ambiente:**

    Crie um arquivo `.env` na raiz do projeto com suas chaves e credenciais.

    ```ini

    DJANGO_SECRET_KEY='sua-chave-secreta-aqui'

    DJANGO_DEBUG='True'

    EMAIL_HOST_USER='seu-email@gmail.com'

    EMAIL_HOST_PASSWORD='sua-senha-de-app-do-google'

    ```

5.  **Execute as migrações e crie um superusuário (opcional):**

    ```bash

    python manage.py migrate

    python manage.py createsuperuser

    ```



### Iniciar a Aplicação



```bash

python manage.py runserver

```



Acesse o projeto em `http://127.0.0.1:8000`.



## 📝 Licença



Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.



## 🤝 Contribuições



Sinta-se à vontade para contribuir\! Para propor melhorias ou relatar bugs, abra uma `issue` ou crie um `pull request`.



## 👨‍💻 Autor



  - [HenriqueCastro18](https://github.com/HenriqueCastro18)

