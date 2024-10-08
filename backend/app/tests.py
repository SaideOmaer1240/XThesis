import subprocess

class LaTeXToDocxConverter:
    def __init__(self, pandoc_path):
        self.pandoc_path = pandoc_path

    def convert(self, latex_content, output_docx_path='output.docx'):
        # Caminho temporário para o arquivo LaTeX
        temp_tex_path = 'temp.tex'

        # Escrever o conteúdo em LaTeX para um arquivo temporário
        with open(temp_tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        # Comando para converter o arquivo LaTeX para DOCX usando Pandoc
        command = [
            self.pandoc_path,
            temp_tex_path,  # Arquivo de entrada
            '-o', output_docx_path  # Arquivo de saída
        ]

        # Executar o comando
        subprocess.run(command)

        print(f"Conversão concluída. O arquivo {output_docx_path} foi criado.")

# Uso da classe
pandoc_path = 'C:/Users/Cristina Setimane/AppData/Local/Pandoc/pandoc.exe'
converter = LaTeXToDocxConverter(pandoc_path)


# Conteúdo LaTeX com cálculos verticais e Bhaskara
latex_content = r"""
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Exercícios de Cálculo}

\subsection*{1. Cálculo de Limite}
Calcule o seguinte limite:

\[
\lim_{{x \to 2}} \frac{{x^2 - 4}}{{x - 2}}
\]

\textbf{Solução:}

Primeiro, simplificamos a expressão:

\[
\frac{{x^2 - 4}}{{x - 2}} = \frac{{(x-2)(x+2)}}{{x-2}}
\]

Cancelamos o termo \(x-2\):

\[
= x + 2
\]

Aplicamos o limite substituindo \(x = 2\):

\[
\lim_{{x \to 2}} (x + 2) = 2 + 2 = 4
\]

\subsection*{2. Cálculo de Infinitesimais}
Considere a função \( f(x) = x^3 \) e calcule o limite infinitesimal quando \( x \) tende a zero:

\[
\lim_{{x \to 0}} \frac{{f(x)}}{{x}} = \lim_{{x \to 0}} \frac{{x^3}}{{x}} 
\]

Simplificamos a expressão:

\[
= \lim_{{x \to 0}} x^2
\]

Como \( x \) tende a zero:

\[
= 0
\]

\subsection*{3. Limite Infinitamente Grande}
Calcule o seguinte limite quando \( x \) tende ao infinito:

\[
\lim_{{x \to \infty}} \frac{{5x^2 + 3x}}{{2x^2 - x + 1}}
\]

Dividimos numerador e denominador pelo termo de maior grau \(x^2\):

\[
= \lim_{{x \to \infty}} \frac{{5 + \frac{3}{x}}}{{2 - \frac{1}{x} + \frac{1}{x^2}}}
\]

Aplicamos o limite \( x \to \infty \):

\[
= \frac{5}{2}
\]

Portanto, o limite é \( \frac{5}{2} \).

\section*{Exercícios de Bhaskara}

\subsection*{1. Solução de Equação Quadrática}
Resolva a equação quadrática:

\[
ax^2 + bx + c = 0
\]

Onde \( a = 1 \), \( b = -3 \) e \( c = 2 \).

\textbf{Solução:}

Primeiro, identificamos os coeficientes:

\[
a = 1, \quad b = -3, \quad c = 2
\]

Aplicamos a fórmula de Bhaskara:

\[
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\]

Calculamos o discriminante:

\[
\Delta = b^2 - 4ac = (-3)^2 - 4 \cdot 1 \cdot 2 = 9 - 8 = 1
\]

Substituímos os valores na fórmula:

\[
x_1 = \frac{-(-3) + \sqrt{1}}{2 \cdot 1} = \frac{3 + 1}{2} = \frac{4}{2} = 2
\]

\[
x_2 = \frac{-(-3) - \sqrt{1}}{2 \cdot 1} = \frac{3 - 1}{2} = \frac{2}{2} = 1
\]

Portanto, as raízes da equação são \( x_1 = 2 \) e \( x_2 = 1 \).

\end{document}
"""

# Converter para DOCX
converter.convert(latex_content, 'exercicios_calculo_bhaskara_vertical.docx')
