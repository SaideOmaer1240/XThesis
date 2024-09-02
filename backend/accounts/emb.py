import textwrap
import google.generativeai as genai
import pandas as pd
import numpy as np
import pypdf
from tkinter import filedialog
# Configuração da API
GOOGLE_API_KEY = 'AIzaSyCV6Tu-b2gn9Xd1mkBt34zx2R5334HEwoA'
genai.configure(api_key=GOOGLE_API_KEY)

# Função para gerar embeddings
def gerar_embedding(texto):
    modelo = 'models/embedding-001'
    blocos = textwrap.wrap(texto, 1000)
    embeddings = []
    for bloco in blocos:
        embedding = genai.embed_content(model=modelo, content=bloco, task_type="retrieval_document")
        embeddings.append(embedding['embedding'])
    return np.mean(embeddings, axis=0)

# Função para extrair texto de um PDF
def extrair_texto_pdf(caminho_pdf):
    texto_completo = ""
    with open(caminho_pdf, 'rb') as arquivo_pdf:
        leitor_pdf = pypdf.PdfReader(arquivo_pdf)
        for pagina in range(len(leitor_pdf.pages)):
            texto_pagina = leitor_pdf.pages[pagina].extract_text()
            texto_completo += texto_pagina
    return texto_completo

# Exemplo: Extrair texto de um PDF específico
caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
texto_pdf = extrair_texto_pdf(caminho_pdf)

# Gerar embedding para o texto do PDF
embedding_pdf = gerar_embedding(texto_pdf)

# Criar DataFrame com o conteúdo do PDF
df = pd.DataFrame([{'Titulo': 'Documento PDF', 'Texto': texto_pdf, 'embedding': embedding_pdf}])

# Função para calcular similaridade e buscar documentos
def buscar_documento(consulta, df):
    embedding_consulta = gerar_embedding(consulta)
    df['similaridade'] = df['embedding'].apply(lambda x: np.dot(embedding_consulta, x))
    df_ordenado = df.sort_values(by='similaridade', ascending=False)
    return df_ordenado.iloc[0]['Texto'] if not df_ordenado.empty else "Nenhum documento relevante encontrado."

# Exemplo de uso
while True:
    consulta = input("query: ")
    if consulta.lower() == 'sair':
        break
    resposta = buscar_documento(consulta, df)
    print(f"Resposta mais relevante: {resposta}")
