import re

latex = r"""Um arquivo LaTeX é um documento de texto que contém código escrito em LaTeX, uma linguagem de marcação amplamente utilizada para a criação de documentos de alta qualidade, especialmente em contextos acadêmicos, científicos e técnicos. LaTeX é particularmente valorizado pela sua capacidade de lidar com fórmulas matemáticas complexas, bibliografias, citações e referências cruzadas de maneira eficiente. Arquivos LaTeX normalmente têm a extensão `.tex`. Dentro desses arquivos, o conteúdo é estruturado usando comandos específicos que definem a formatação do texto, a organização do documento (como seções, capítulos e parágrafos) e a inclusão de elementos como tabelas, gráficos e fórmulas.

Por exemplo, um simples arquivo LaTeX poderia começar assim:

\documentclass{article}
\begin{document}
\title{Meu Primeiro Documento LaTeX}
\author{Saíde Omar Saíde}
\date{\today}
\maketitle
\section{Introdução}
Este é o meu primeiro documento escrito em LaTeX.
\end{document}

Esse código geraria um documento com um título, o nome do autor, a data e uma seção intitulada Introdução

Para visualizar ou gerar o documento final, o arquivo `.tex` é processado por um compilador LaTeX, que converte o código em um arquivo PDF, DVI, ou outro formato de saída.
"""
def get_latex_content(text):
    # Usando uma expressão regular para extrair o conteúdo LaTeX
    pattern = r"\\documentclass\{.*?\}.*?\\end\{document\}"
    latex_code = re.search(pattern, text, re.DOTALL).group(0)
    return latex_code

latex_code = get_latex_content(latex)

# Salvando o conteúdo LaTeX em um arquivo .tex
with open("documenton.tex", "w") as tex_file:
    tex_file.write(latex_code)

