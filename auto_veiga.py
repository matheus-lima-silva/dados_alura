import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
import os

load_dotenv()

class TestOpenrequest1():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def test_openrequest1(self):
    # Test name: open_request_1
    # Step # | name | target | value | comment
    # 1 | open | /Login |  | 
    self.driver.get("https://portalaluno.uva.br/Login")
    # 2 | setWindowSize | 1920x1080 |  | 
    self.driver.set_window_size(1920, 1080)
    # 3 | type | id=LoginEntrada_login | 17163934777 | 
    self.driver.find_element(By.ID, "LoginEntrada_login").send_keys(os.getenv('login_veiga'))
    # 4 | type | id=LoginEntrada_senha | UVA@27041997 | 
    self.driver.find_element(By.ID, "LoginEntrada_senha").send_keys(os.getenv('senha_veiga'))
    # 5 | click | id=btn_logar |  | 
    self.driver.find_element(By.ID, "btn_logar").click()
    # 6 | click | id=imgBanner |  | 
    self.vars["window_handles"] = self.driver.window_handles
    # 7 | selectWindow | handle=${win7377} |  | 
    self.driver.find_element(By.ID, "imgBanner").click()
    # 8 | click | xpath=//div[2]/ion-header-bar/div/span/button |  | 
    self.vars["win7377"] = self.wait_for_window(2000)
    # 9 | click | linkText=Secretaria Virtual |  | 
    self.driver.switch_to.window(self.vars["win7377"])
    # 10 | click | xpath=//ion-item[6]/div/a/span |  | 
    self.driver.find_element(By.XPATH, "//div[2]/ion-header-bar/div/span/button").click()
    # 11 | verifyElementPresent | xpath=//button[@id='btAdicionarServico'] |  | 
    self.driver.find_element(By.LINK_TEXT, "Secretaria Virtual").click()
    # 12 | click | id=btAdicionarServico |  | 
    self.driver.find_element(By.XPATH, "//ion-item[6]/div/a/span").click()
    # 13 | runScript | window.scrollTo(0,0) |  | 
    elements = self.driver.find_elements(By.XPATH, "//button[@id=\'btAdicionarServico\']")
    assert len(elements) > 0
    # 14 | click | xpath=//ion-side-menu-content[@id='ion-side-menu-content']/ion-nav-view/div/ion-view/ion-content/div/content/div/header/div/button[2] |  | 
    self.driver.find_element(By.ID, "btAdicionarServico").click()
    # 15 | click | css=.ng-untouched |  | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 16 | type | css=.ng-untouched | Comprovação de atividade complementar (alunos matriculados) | 
    self.driver.find_element(By.XPATH, "//ion-side-menu-content[@id=\'ion-side-menu-content\']/ion-nav-view/div/ion-view/ion-content/div/content/div/header/div/button[2]").click()
    # 17 | click | css=.linha > #btConcluirSolicitacao |  | 
    self.driver.find_element(By.CSS_SELECTOR, ".ng-untouched").click()
    # 18 | runScript | window.scrollTo(0,0) |  | 
    self.driver.find_element(By.CSS_SELECTOR, ".ng-untouched").send_keys("Comprovação de atividade complementar (alunos matriculados)")
    # 19 | click | name=Nome do Evento |  | 
    self.driver.find_element(By.CSS_SELECTOR, ".linha > #btConcluirSolicitacao").click()
    # 20 | type | name=Nome do Evento | teste | 
    self.driver.execute_script("window.scrollTo(0,0)")
    # 21 | type | name=Data Início | 2024-09-01 | 
    self.driver.find_element(By.NAME, "Nome do Evento").click()
    # 22 | type | name=Data Término | 2024-09-07 | 
    self.driver.find_element(By.NAME, "Nome do Evento").send_keys("teste")
    # 23 | click | name=Atividade |  | 
    self.driver.find_element(By.NAME, "Data Início").send_keys("2024-09-01")
    # 24 | select | name=Atividade | label=UVA-ENSINO-II - CURSO DE CERTIFICAÇÃO | 
    self.driver.find_element(By.NAME, "Data Término").send_keys("2024-09-07")
    # 25 | type | name=Carga Horária | 7 | 
    self.driver.find_element(By.NAME, "Atividade").click()
    # 26 | click | name=codArquivo |  | 
    dropdown = self.driver.find_element(By.NAME, "Atividade")
    dropdown.find_element(By.XPATH, "//option[. = 'UVA-ENSINO-II - CURSO DE CERTIFICAÇÃO']").click()
    # 27 | click | name=codArquivo |  | 
    self.driver.find_element(By.NAME, "Carga Horária").send_keys("7")
    # 28 | type | css=label:nth-child(19) > input | C:\fakepath\login_lyceum.side | 
    self.driver.find_element(By.NAME, "codArquivo").click()
    self.driver.find_element(By.NAME, "codArquivo").click()
    self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(19) > input").send_keys("/home/matheus/py_estudos/dados_alura/requirements/requirements.txt")
    print("Teste finalizado com sucesso")
