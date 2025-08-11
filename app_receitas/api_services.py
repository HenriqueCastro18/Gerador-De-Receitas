# D:\Freela\Receitas\app_receitas\api_services.py

import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configuração de logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Configuração da API do Google Translate
GOOGLE_TRANSLATE_BASE_URL = 'https://translate.google.com/m'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

class TheMealDB:
    def __init__(self):
        # A API Key da TheMealDB é a mesma para todos os usuários
        self.THEMEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
        self.session = requests.Session()

    def _traduzir_texto_para_portugues(self, texto, sl='en', tl='pt'):
        """Método interno para traduzir texto."""
        if not texto:
            return ""
        
        params = {
            'tl': tl,
            'sl': sl,
            'q': texto
        }
        
        try:
            response = self.session.get(GOOGLE_TRANSLATE_BASE_URL, params=params, headers=HEADERS, timeout=5)
            response.raise_for_status()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            traducao = soup.find('div', class_='result-container').text
            return traducao
        except requests.exceptions.RequestException as e:
            logging.error(f"ERRO TRADUCAO: Falha ao traduzir o texto: {e}")
            return texto
        except Exception as e:
            logging.error(f"ERRO TRADUCAO: Erro inesperado: {e}")
            return texto

    def _traduzir_ingredientes_para_ingles(self, ingredientes_pt):
        """Método interno para traduzir ingredientes."""
        if not ingredientes_pt:
            return []

        ingredientes_en = []
        for ingrediente in ingredientes_pt:
            traducao = self._traduzir_texto_para_portugues(ingrediente, sl='pt', tl='en')
            if traducao:
                ingredientes_en.append(traducao)
        
        return ingredientes_en

    def search(self, ingredientes=None, area=None, categoria=None):
        """Busca receitas na API TheMealDB."""
        url = f"{self.THEMEALDB_BASE_URL}filter.php?"
        params = {}
        
        if ingredientes:
            ingredientes_en = self._traduzir_ingredientes_para_ingles(ingredientes.split(','))
            if ingredientes_en:
                params['i'] = ingredientes_en[0]
                logging.debug(f"Buscando na TheMealDB com ingrediente: {ingredientes_en}")

        if area:
            params['a'] = area
            logging.debug(f"Buscando na TheMealDB por área: {area}")

        if categoria:
            params['c'] = categoria
            logging.debug(f"Buscando na TheMealDB por categoria: {categoria}")

        if not params:
            logging.warning("AVISO: Nenhuma opção de busca fornecida para a API TheMealDB.")
            return []

        try:
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            logging.debug(f"Status da resposta da API: {response.status_code}")
            
            receitas = data.get('meals', [])
            if receitas is None:
                return []
            return receitas
        
        except requests.exceptions.RequestException as e:
            logging.error(f"ERRO API: Falha ao se conectar com a TheMealDB: {e}")
            return []
        except Exception as e:
            logging.error(f"ERRO API: Um erro inesperado ocorreu: {e}")
            return []

    def get_meal_by_id(self, recipe_id):
        """Busca detalhes de uma receita específica na TheMealDB por ID."""
        try:
            meal_id = recipe_id.replace('themealdb_', '')
            url = f"{self.THEMEALDB_BASE_URL}lookup.php?i={meal_id}"
            logging.debug(f"Buscando detalhes da receita com ID: {meal_id}")
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            meal = data.get('meals')[0]

            if not meal:
                logging.error(f"ERRO API DETALHES: Nenhuma receita encontrada para o ID {meal_id}")
                return None

            ingredientes_nomes_e_medidas = []
            for i in range(1, 21):
                ingrediente = meal.get(f'strIngredient{i}')
                medida = meal.get(f'strMeasure{i}')
                if ingrediente and ingrediente.strip():
                    ingrediente_nome_pt = self._traduzir_texto_para_portugues(ingrediente)
                    if medida and medida.strip():
                        medida_pt = self._traduzir_texto_para_portugues(medida)
                        ingredientes_nomes_e_medidas.append(f"{medida_pt} de {ingrediente_nome_pt}")
                    else:
                        ingredientes_nomes_e_medidas.append(ingrediente_nome_pt)

            nome_pt = self._traduzir_texto_para_portugues(meal.get('strMeal', 'Receita Sem Nome'))
            modo_preparo_pt = self._traduzir_texto_para_portugues(meal.get('strInstructions', ''))

            receita_formatada = {
                'id': f"themealdb_{meal['idMeal']}",
                'nome': nome_pt,
                'imagem_url': meal.get('strMealThumb', ''),
                'tempo_preparo_minutos': None,
                'ingredientes_nomes': ingredientes_nomes_e_medidas,
                'modo_preparo': modo_preparo_pt,
                'link_externo': meal.get('strSource', ''),
                'fonte': 'TheMealDB',
            }

            return receita_formatada

        except (requests.exceptions.RequestException, IndexError, KeyError) as e:
            logging.error(f"ERRO API DETALHES: Erro ao buscar detalhes da receita {recipe_id} na TheMealDB: {e}")
            return None
        except Exception as e:
            logging.error(f"ERRO API DETALHES: Um erro inesperado ocorreu: {e}")
            return None