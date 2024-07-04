'''from scholarly import scholarly




 

# Buscar por artigos diretamente
search_query = scholarly.search_pubs('anfibios')
for i in range(3):  # Limitar a 3 resultados para exemplo
    article = next(search_query)
    print(f"Titulo: {article['bib']['title']}")
    print(f"Autores: {article['bib']['author']}")
    print(f"Ano: {article['bib']['pub_year']}")
    print(f"Resumo: {article['bib'].get('abstract', 'Sem resumo disponível')}")
    print()
'''
import re
from docx import Document

class DocumentFormatter:
    def add_formatted_text(self, document, text):
        # Expressão regular para encontrar texto entre <p> e </p>
        p_pattern = re.compile(r'<p>(.*?)</p>')
        p_matches = p_pattern.findall(text)
        
        for p_match in p_matches:
            paragraph = document.add_paragraph()
            # Expressão regular para encontrar texto entre <strong> e </strong>
            strong_pattern = re.compile(r'<strong>(.*?)</strong>')
            parts = strong_pattern.split(p_match)
            
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Textos entre <strong> tags
                    run = paragraph.add_run(part)
                    run.bold = True
                else:  # Textos fora das <strong> tags
                    paragraph.add_run(part)
        
        # Expressão regular para encontrar texto entre <li> e </li>
        li_pattern = re.compile(r'<li>(.*?)</li>')
        li_matches = li_pattern.findall(text)
        
        for li_match in li_matches:
            # Adiciona o texto encontrado como item de lista com estilo 'List Bullet'
            paragraph = document.add_paragraph(style='List Bullet')
            paragraph.add_run(li_match)

# Exemplo de uso
doc = Document()
formatter = DocumentFormatter()
text = "<p>Tópico: <strong>Exemplo de Tópico</strong></p> e mais texto aqui <p>Outro <strong>Tópico Importante</strong></p><li>Primeiro item de lista</li><li>Segundo item de lista</li>"
formatter.add_formatted_text(doc, text)

# Salvar o documento
doc.save("documento_formatado.docx")
