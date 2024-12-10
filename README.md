# Automação de Envio de Certificados Alura

## Descrição do Projeto

Este projeto automatiza o processo de extração de dados de cursos da Alura, geração de PDFs dos certificados e envio para a Universidade Veiga de Almeida (UVA) para contabilização de horas complementares. 🎓

**Motivação:**

Cansado de baixar seus certificados da Alura e enviar manualmente para a UVA ( Universidade Veiga de Almeida) para contabilizar horas complementares? Este projeto resolve esse problema! 🚀

## Funcionalidades

* **Extração de dados:** Extrai informações relevantes dos cursos da Alura, como nome, data de início, data de término e carga horária.
* **Geração de PDFs:** Gera PDFs dos certificados a partir dos links da Alura.
* **Automação de formulário:** Preenche automaticamente o formulário de comprovação de atividade complementar da UVA.
* **Registro de logs:** Gera logs detalhados de todo o processo para facilitar a identificação de problemas.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Selenium:** Automação web.
* **BeautifulSoup:** Web scraping.
* **Pandas:** Manipulação de dados.
* **pdfkit:** Geração de PDFs.
* **dotenv:** Gerenciamento de variáveis de ambiente.
* **logging:** Registro de logs.

## Como usar

1. **Clone o repositório:** `git clone https://github.com/matheus-lima-silva/dados_alura.git`
2. **Faça o download da sua página de cursos:**
    * Acesse a página do seu perfil na Alura: `https://cursos.alura.com.br/user/seuusuario` (substitua `seuusuario` pelo seu nome de usuário).
    * Salve a página como um arquivo HTML na pasta `pagina_cursos_html`.
3. **Instale as dependências:** `pip install -r requirements.txt`
4. **Configure as variáveis de ambiente:**
    * Crie um arquivo `.env` na raiz do projeto.
    * Adicione as seguintes variáveis:
        ```
        login_veiga=seu_login_uva
        senha_veiga=sua_senha_uva
        ```
5. **Execute o script principal:** `python setup.py`

## Estrutura do Projeto

* **setup.py:** Orquestra todo o processo de automação.
* **DataScraping.py:** Contém a classe `RaspagemDados` para extração de dados.
* **PDFGenerator.py:** Contém a classe `PDFGenerator` para geração de PDFs.
* **AutomacaoFormulario.py:** Contém a classe `AutomacaoFormulario` para automação do formulário.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests. 😊

## Observações

* Certifique-se de ter o ChromeDriver instalado e configurado corretamente.
* Este projeto foi desenvolvido para uso pessoal e pode precisar de adaptações para funcionar em outros ambientes.
