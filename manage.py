#!/usr/bin/env python
"""
Este é o utilitário de linha de comando do Django para tarefas administrativas.
Eu achei melhor deixar o arquivo padrão do Django, pois ele já tem toda a
estrutura necessária para executar comandos como 'runserver', 'migrate',
'createsuperuser' e muitos outros. Mudar isso poderia causar erros inesperados
e não traria nenhum benefício para o projeto.
"""
import os
import sys


def main():
    """
    Esta é a função principal que executa as tarefas administrativas do Django.
    Eu criei esta função para encapsular toda a lógica de execução.
    """
    # Aqui eu defino a variável de ambiente para o módulo de configurações do Django.
    # Eu configurei para que ela aponte para 'gerador_receitas.settings', que é
    # onde todas as configurações do meu projeto estão salvas. Isso é essencial
    # para que o Django saiba onde encontrar as configurações corretas.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gerador_receitas.settings')
    try:
        # Eu importei a função 'execute_from_command_line' para processar
        # os comandos que o usuário digita no terminal.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Este bloco 'try-except' é uma segurança. Se o Django não estiver
        # instalado ou o ambiente virtual não estiver ativado, este erro
        # personalizado será levantado. Eu achei importante ter uma mensagem
        # de erro clara para ajudar outros desenvolvedores (ou eu mesmo no futuro)
        # a resolver problemas de configuração rapidamente.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Finalmente, eu executo o comando que foi passado pela linha de comando.
    # Por exemplo, se eu digitei 'python manage.py runserver', esta linha
    # é responsável por iniciar o servidor de desenvolvimento.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Este é um 'entry point' padrão do Python. A verificação 'if __name__ == "__main__"'
    # garante que a função 'main' será executada apenas se o arquivo for rodado
    # diretamente, e não se for importado como um módulo em outro lugar.
    # Eu achei melhor manter essa prática padrão, pois é robusta e bem entendida.
    main()