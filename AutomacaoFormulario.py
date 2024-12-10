import time
import os
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

logging.basicConfig(filename='automacao.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class AutomacaoFormulario:
    def __init__(self, url, raspagem_dados=None, csv_path=None, timeout=30):
        self.url = url
        self.raspagem_dados = raspagem_dados
        self.csv_path = csv_path or '/home/matheus/py_estudos/dados_alura/cursos.csv'
        self.timeout = timeout

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--lang=pt-BR")
        
        caminho_chromedriver = "/home/matheus/.cache/selenium/chromedriver/linux64/130.0.6723.116/chromedriver"  
        self.service = Service(caminho_chromedriver)
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.vars = {}

        load_dotenv()

    def iniciar(self):
        try:
            if self.csv_path and os.path.exists(self.csv_path):
                logging.info("Carregando dados do arquivo CSV.")
                self.dados_certificados = pd.read_csv(self.csv_path)
            else:
                logging.info("CSV não encontrado ou inválido. Extraindo dados por raspagem.")
                self.dados_certificados = self.raspagem_dados.extrair_dados()

            if not self.dados_certificados.empty:
                self.driver.get(self.url)

                # Realiza o login
                self.realizar_login()

                # Navega até a página do formulário
                self.navegar_pagina_formulario()

                for _, dados in self.dados_certificados.iterrows():
                    self.processar_formulario(dados)

        except Exception as e:
            logging.error("Erro ao iniciar a automação: %s", e)
        finally:
            logging.info("Finalizando a automação.")
            time.sleep(300)
            self.driver.quit()

    def realizar_login(self):
        try:
            logging.info("Iniciando o processo de login.")
            login = os.getenv('login_veiga')
            senha = os.getenv('senha_veiga')

            if not login or not senha:
                raise ValueError("Variáveis de ambiente 'login_veiga' ou 'senha_veiga' não encontradas.")

            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, "LoginEntrada_login"))
            ).send_keys(login)
            self.driver.find_element(By.ID, "LoginEntrada_senha").send_keys(senha)
            self.driver.find_element(By.ID, "btn_logar").click()
            logging.info("Login realizado com sucesso.")
        except Exception as e:
            logging.error("Erro no processo de login: %s", e)

    def navegar_pagina_formulario(self):
        try:
            logging.info("Navegando para a página de 'Secretaria Virtual'.")
            self.driver.get("https://portalaluno.uva.br/SistemasSatelites/SSO?Sistema=1")
            
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, "menu"))
            )
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Virtual Office"))
            ).click()
            logging.info("Redirecionamento completo para a página de 'Secretaria Virtual'.")
            self.driver.get("https://sis.lyceum.com.br/AOnline3/index.html#/home/servico-solicitacao")
        except Exception as e:
            logging.error("Erro na navegação até a página do formulário: %s", e)

    def processar_formulario(self, dados):
        try:
            # Fecha o modal se estiver aberto
            try:
                close_button = self.driver.find_element(By.CLASS_NAME, "close")
                if close_button.is_displayed():
                    close_button.click()
            except NoSuchElementException:
                pass

            WebDriverWait(self.driver, self.timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
            )

            # Clica em 'Adicionar Serviço' usando JavaScript para garantir interação
            adicionar_servico_button = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.ID, "btAdicionarServico"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", adicionar_servico_button)
            self.driver.execute_script("arguments[0].click();", adicionar_servico_button)
            logging.info("Clicou em 'btAdicionarServico'")
            
            # Espera pelo input do próximo passo e preenche os campos do formulário
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.cron-form-control"))
            )

            input_element = self.driver.find_element(By.CSS_SELECTOR, "input.cron-form-control")
            self.driver.execute_script("arguments[0].click();", input_element)
            self.driver.find_element(By.CSS_SELECTOR, ".ng-untouched").send_keys("Comprovação de atividade complementar (alunos matriculados)")

            # Aguarda o botão "Next" estar clicável e clica usando JavaScript para garantir a interação
            botao_next = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Comprovação de Atividade Complementar (alunos matriculados)')]/following-sibling::button"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", botao_next)
            self.driver.execute_script("arguments[0].click();", botao_next)
            logging.info("Clicou em 'Next' para o serviço.")

            # Preenche os campos do formulário
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.NAME, "Nome do Evento"))
            ).send_keys(str(dados['titulo_curso']))
            logging.info("Nome do evento preenchido com sucesso.")
            
            date_field = self.driver.find_element(By.NAME, "Data Início")
            date_field.clear()
            date_field.send_keys(str(dados['data_inicio']))  # Insere a data diretamente (dd/mm/yyyy)
            logging.info("Data de início preenchida com sucesso.")
            date_field = self.driver.find_element(By.NAME, "Data Término")
            date_field.clear()
            date_field.send_keys(str(dados['data_final']))  # Insere a data diretamente (dd/mm/yyyy)
            logging.info("Data de início preenchida com sucesso.")


            dropdown_atividade = Select(self.driver.find_element(By.NAME, "Atividade"))
            WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.NAME, "Atividade"))
            )
            dropdown_atividade.select_by_visible_text("UVA-ENSINO-II - CURSO DE CERTIFICAÇÃO")
            logging.info("Atividade selecionada com sucesso.")

            carga_horaria_input = self.driver.find_element(By.NAME, "Carga Horária")
            carga_horaria_input.clear()
            carga_horaria_input.send_keys(str(dados['horas']))
            logging.info("Carga horária preenchida com sucesso.")

            input_arquivo = self.driver.find_element(By.CSS_SELECTOR, "input[type='file'][name='codArquivo']")
            input_arquivo.send_keys(dados['path'])
            logging.info("Arquivo do certificado enviado com sucesso.")

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            botao_concluir = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.ID, "btConcluirServico"))
            )
            
            botao_concluir.click()
            logging.info("Botão 'btConcluirServico' clicado com sucesso.")
            logging.info("Formulário preenchido e submetido com sucesso para o curso: %s", dados['titulo_curso'])

        except NoSuchElementException as e:
            logging.error("Erro: Elemento não encontrado ao interagir com o formulário: %s", e)            
        except TimeoutException as e:
            logging.error("Erro: Timeout ao interagir com o formulário: %s", e)            
        except Exception as e:
            logging.exception("Ocorreu um erro ao interagir com o formulário: %s", e)
