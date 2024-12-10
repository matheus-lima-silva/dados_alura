import DataScraping as ds
import PDFGenerator
from AutomacaoFormulario import AutomacaoFormulario  # Importe a classe corretamente

scraper = ds.RaspagemDados(
    html_path='/home/matheus/py_estudos/dados_alura/pagina_cursos_html/Perfil de Matheus Lima silva _ Alura - Cursos online de tecnologia.html',
    css_selector='.news__item .header-news-item--highlighted',
    output_dir='/home/matheus/py_estudos/dados_alura/certificados'
)
df = scraper.extrair_dados()

for df_index, row in df.iterrows():
    pdf_generator = PDFGenerator.PDFGenerator()
    pdf_generator.gerar_pdf(row['link'], row['titulo_curso'])

# Instancie a classe AutomacaoFormulario corretamente
subir_arquivos = AutomacaoFormulario(
    url='https://portalaluno.uva.br/Login',
    raspagem_dados=scraper
)
subir_arquivos.iniciar()

