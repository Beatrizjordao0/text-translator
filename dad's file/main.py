from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from fpdf import FPDF


def ler_pdf(caminho_pdf):
    with open(caminho_pdf, "rb") as arquivo:
        leitor_pdf = PdfReader(arquivo)
        texto = ""
        for pagina in range(len(leitor_pdf.pages)):
            texto += leitor_pdf.pages[pagina].extract_text()
    return texto


def dividir_texto(texto, tamanho_maximo=5000):
    texto = texto.strip()
    partes = []
    while len(texto) > tamanho_maximo:
        corte = texto[:tamanho_maximo].rfind(' ')
        if corte == -1:
            corte = tamanho_maximo
        partes.append(texto[:corte].strip())
        texto = texto[corte:].strip()
    if texto:
        partes.append(texto)
    return partes


def traduzir_texto(texto, idioma_destino="pt"):
    tradutor = GoogleTranslator(source='auto', target=idioma_destino)
    partes_texto = dividir_texto(texto)
    traducao_completa = ""
    for parte in partes_texto:
        traducao_completa += tradutor.translate(parte)
    return traducao_completa


def criar_pdf(texto_traduzido, caminho_pdf_saida):
    pdf = FPDF()
    pdf.add_page()

    # Registrar fonte TTF (precisa estar no diretório do projeto)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    for linha in texto_traduzido.split("\n"):
        pdf.multi_cell(0, 10, linha)

    pdf.output(caminho_pdf_saida)


# Exemplo de uso:
caminho_pdf_entrada = "manual.pdf"
caminho_pdf_saida = "manual_pt.pdf"

texto_original = ler_pdf(caminho_pdf_entrada)
texto_traduzido = traduzir_texto(texto_original, idioma_destino="pt")
criar_pdf(texto_traduzido, caminho_pdf_saida)
