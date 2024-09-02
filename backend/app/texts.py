import re

text = """"""

# Expressão regular para capturar o conteúdo entre os blocos de três acentos graves e a palavra-chave 'latex'
pattern = r'```latex\s*([\s\S]*?)```'
match = re.search(pattern, text)

if match:
    latex_code = match.group(1).strip()
    print(latex_code)
