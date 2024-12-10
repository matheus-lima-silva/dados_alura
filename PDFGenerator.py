import os

try:
    import pdfkit
except ImportError:
    pdfkit = None

class PDFGenerator:
    """
    Uma classe para gerar PDFs a partir de URLs.
    Atributos:
    ----------
    output_dir : str
        O diretório onde os PDFs gerados serão salvos.
    Métodos:
    --------
    gerar_pdf(url, filename):
        Gera um PDF a partir da URL fornecida e salva com o nome de arquivo especificado.
    """
    def __init__(self, output_dir="pdfs"):
        self.output_dir = output_dir

    def gerar_pdf(self, url, filename):
      

        output_path = os.path.join(self.output_dir, f"{filename}.pdf")

        # Verifica se o arquivo já existe
        if os.path.exists(output_path):
            print(f"O arquivo PDF já existe: {output_path}")
            return

        try:
            # Verifica e cria o diretório
            os.makedirs(self.output_dir, exist_ok=True)

            # Verifica se o pdfkit está disponível
            if pdfkit is None:
                print("Erro: pdfkit não está disponível. Certifique-se de que o pacote pdfkit está instalado.")
                return

            # Gera o PDF
            pdfkit.from_url(url, output_path, options={'quiet': ''})
            print(f"PDF gerado com sucesso: {output_path}")
        except Exception as e:
            print(f"Erro ao gerar o PDF: {str(e)}")