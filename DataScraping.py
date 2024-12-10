import pandas as pd
"""
Este módulo fornece funcionalidades para raspagem de dados de cursos a partir de um arquivo HTML e extração de informações adicionais da web.
Classes:
    RaspagemDados: Uma classe para lidar com a raspagem e extração de dados de cursos.
Métodos:
    __init__(self, html_path, css_selector, output_dir):
        Inicializa a instância de RaspagemDados com o caminho do arquivo HTML, seletor CSS e diretório de saída fornecidos.
    extrair_dados(self):
        Extrai dados de cursos do arquivo HTML especificado por html_path.
        Retorna um DataFrame do pandas contendo os dados dos cursos.
    extrair_horas(self, url):
        Extrai o número de horas a partir da URL fornecida.
        Retorna o número de horas como uma string se encontrado, caso contrário retorna None.
"""
from bs4 import BeautifulSoup
import re
import requests

class RaspagemDados:
    def __init__(self, html_path, css_selector, output_dir):
        self.html_path = html_path
        self.css_selector = css_selector
        self.output_dir = output_dir

    def extrair_dados(self):
        with open(self.html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        course_items = soup.find_all('li', class_='card-list__item')

        course = []
        for item in course_items:
            titulo_curso = item.find('span', class_="course-card__name")
            data_inicio = item.find('span', class_="course-card__start-date").text.strip().split(': ')[1]
            data_final = item.find('span', class_="course-card__finish-date").text.strip().split(': ')[1]
            link = item.find('a',class_="course-card__certificate bootcamp-text-color")['href']
            link = link.replace('/certificate','/formalCertificate')
            course.append({
                'titulo_curso': titulo_curso.text,
                'data_inicio': data_inicio,
                'data_final': data_final,
                'link': link,
                'horas': self.extrair_horas(link),
                'path' : f'//home/matheus/py_estudos/dados_alura/certificados/{titulo_curso.text}.pdf'})
        return pd.DataFrame(course)
    
    def extrair_horas(self, url):
        seletor_css = 'body > div.formal-certificate-topics.certificate-details > span'  # Seletor CSS mais específico

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.select_one(seletor_css)

            if element:
                texto_completo = element.get_text(strip=True)

                # Expressão regular mais precisa
                match = re.search(r'carga horária estimada em (\d+) horas', texto_completo, re.IGNORECASE)
                if match:
                    return match.group(1)
                else:
                    print(f"Não foi possível encontrar o número de horas em '{texto_completo}'")
            else:
                print(f"Elemento com seletor '{seletor_css}' não encontrado.")

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None