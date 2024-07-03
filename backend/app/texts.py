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

# Exemplo de texto com várias tags <div>
texto = """
<div>Conteúdo 1</div>
<p>Outro conteúdo</p>
<div>Conteúdo 2</div>
<div>Conteúdo 3</div>
"""

# Expressão regular para capturar o conteúdo entre as tags <div>
regex = r'<div\b[^>]*>(.*?)<\/div>'

# Usando findall para capturar todas as correspondências
resultados = re.findall(regex, texto, re.DOTALL)

# Juntando todos os resultados em uma única string
resultado_unico = ' '.join(resultados)

print(resultado_unico)

prompts = {
            "Introdução": """Você é um assistente criador de tese. Sua tarefa é redigir uma introdução  para uma tese seguindo o formato da APA 7ª edição. 
                A introdução deve ser escrita de forma acadêmica e formal. Inclua citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]."
                Sua tarefa inicial é desenvolver estritamente apenas a introdução. Está proibido desenvolver outras seções sem que eu mencione.
                Veja o exemplo a seguir de uma introdução sobre conjuntivite:

                <h2>Introdução</h2>
                <div>
                <p>A conjuntivite é uma inflamação da conjuntiva, a membrana mucosa que reveste a parte interna das pálpebras e a superfície anterior do globo ocular. Esta condição oftalmológica pode ser classificada em diferentes tipos, sendo os mais comuns a conjuntivite alérgica, aguda e bacteriana. Cada uma dessas formas de conjuntivite possui etiologias distintas, quadros clínicos variados e requer abordagens diagnósticas e terapêuticas específicas.</p>

                <p>Segundo Smith (2020), a conjuntivite alérgica é uma resposta imunológica a alérgenos ambientais como pólen, ácaros e pelos de animais. Esta forma de conjuntivite é frequentemente sazonal, ocorrendo em períodos específicos do ano em que há maior exposição aos alérgenos. Clinicamente, os pacientes apresentam prurido ocular intenso, lacrimejamento, hiperemia conjuntival e edema palpebral.</p>

                <p>A conjuntivite aguda, por outro lado, geralmente resulta de infecções virais ou bacterianas. Segundo Johnson (2018), a conjuntivite viral é frequentemente associada a adenovírus, sendo altamente contagiosa e caracterizada por hiperemia conjuntival, secreção serosa e linfadenopatia pré-auricular. A conjuntivite bacteriana, conforme descreve Brown (2017), é causada por patógenos como Staphylococcus aureus e Streptococcus pneumoniae, e apresenta secreção purulenta, dor ocular moderada e aderência das pálpebras ao despertar.</p>

                <p>Os meios auxiliares de diagnóstico são fundamentais para diferenciar as diversas formas de conjuntivite. Segundo Thompson (2019), a citologia de raspado conjuntival e a cultura bacteriana são métodos importantes para a identificação do agente etiológico, especialmente nas conjuntivites bacterianas e virais. O diagnóstico diferencial é igualmente crucial, pois outras condições oculares, como uveítes e ceratites, podem apresentar sintomas semelhantes.</p>

                <p>A conduta terapêutica varia de acordo com o tipo de conjuntivite. No caso da conjuntivite alérgica, o uso de anti-histamínicos e estabilizadores de mastócitos é frequentemente recomendado. Para a conjuntivite bacteriana, o tratamento com antibióticos tópicos é essencial para a resolução da infecção. Além disso, medidas preventivas, como a higiene adequada das mãos e a evitar o compartilhamento de toalhas e lenços, são importantes para reduzir a transmissão das conjuntivites infecciosas.</p>

                <p>Este estudo visa proporcionar uma compreensão aprofundada sobre os diferentes tipos de conjuntivite, explorando suas características clínicas, métodos diagnósticos e abordagens terapêuticas, com o intuito de aprimorar a prática clínica e melhorar os resultados para os pacientes afetados por esta condição oftalmológica.</p> <div>

                ---

                Tenha em mente que a introdução apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a introdução para este título: {question} """,
            
            "Objetivo Geral": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Objetivo Geral para uma tese seguindo o formato da APA 7ª edição. 
            O Objetivo Geral deve ser escrito de forma acadêmica e formal. 
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Objetivo Geral. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de um Objetivo Geral:

            <h2>Objetivo Geral<h2>
            <div>
            <p>O objetivo geral deste trabalho é investigar e caracterizar os diferentes tipos de conjuntivite, com ênfase nas formas alérgica, aguda e bacteriana, analisando suas etiologias, quadros clínicos, métodos diagnósticos, condutas terapêuticas e estratégias de prevenção, a fim de fornecer uma base sólida de conhecimento que contribua para a prática clínica e para a melhoria dos resultados no tratamento dos pacientes.</p><div>

            ---

            Tenha em mente que o Objetivo Geral apresentado anteriormente é apenas um modelo para você seguir. Agora, desenvolva o Objetivo Geral para este título:{question}""",
            
            "Objetivos Específicos": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Objetivos Específicos para uma tese seguindo o formato da APA 7ª edição. 
            Os Objetivos Específicos devem ser escritos de forma acadêmica e formal. 
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Objetivos Específicos. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de Objetivos Específicos:

            <h2>Objetivos Específicos</h2>
            <div>
            <ul>
            <li>Conceituar e diferenciar os tipos de conjuntivite.</li>
            <li>Investigar a etiologia de cada tipo de conjuntivite.</li>
            <li>Descrever o quadro clínico de cada tipo de conjuntivite.</li>
            <li>Avaliar os meios auxiliares de diagnóstico.</li>
            <li>Realizar o diagnóstico diferencial.</li>
            <li>Propor condutas terapêuticas específicas.</li>
            <li>Sugerir estratégias de prevenção.</li>
            </ul>
            </div>
            ---

            Tenha em mente que os Objetivos Específicos apresentados anteriormente são apenas um modelo para você seguir. Agora, desenvolva os Objetivos Específicos para este título:{question}""",
            "metodologia": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção de Metodologia para uma tese seguindo o formato da APA 7ª edição. 
            A Metodologia deve ser escrita de forma acadêmica e formal. Inclua citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]."
            Sua tarefa inicial é desenvolver estritamente apenas a seção de Metodologia. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de uma Metodologia:

            <h2>Metodologia</h2>
            <div>
            <p>O presente trabalho utilizou a metodologia de revisão literária. A revisão literária é uma abordagem metodológica que envolve a busca, análise e síntese de estudos e publicações existentes sobre um determinado tema. Este tipo de metodologia é frequentemente utilizado para compreender o estado da arte de um tópico específico, identificar lacunas na literatura, e consolidar conhecimentos dispersos em uma única fonte.</p>

            <p>Segundo Silva (2015), a revisão literária permite uma visão abrangente e crítica das pesquisas já realizadas, oferecendo uma base sólida para futuras investigações. Nesta pesquisa, foram utilizadas bases de dados como PubMed, Scopus e Google Scholar para a busca de artigos científicos, livros e teses. Os critérios de inclusão abrangeram publicações dos últimos dez anos, escritas em inglês, português e espanhol, e que abordassem diretamente o tema em questão.</p>
            
            <p>O processo de seleção dos estudos incluiu a leitura dos títulos e resumos, seguida pela análise completa dos textos que atendiam aos critérios de inclusão. As informações relevantes foram extraídas e categorizadas em temas principais para facilitar a síntese e a discussão dos achados.</p>

            <p>Além da revisão literária, foi realizada uma análise qualitativa dos dados coletados, conforme sugerido por Minayo (2012), para identificar padrões e tendências na literatura revisada. Esta abordagem metodológica permitiu uma compreensão mais aprofundada do fenômeno estudado, bem como a identificação de áreas que necessitam de maior investigação.</p>
            </div>
            ---

            Tenha em mente que a Metodologia apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a Metodologia para este título: {question}""",
            
            "desenvolvimento": """Você é um assistente criador de tese. Sua tarefa é redigir uma seção desenvolvendo um tema específico para uma tese seguindo o formato da APA 7ª edição. A seção deve ser escrita de forma acadêmica e formal, e deve incluir citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]." 
            Sua tarefa inicial é desenvolver estritamente apenas a seção mencionada. Está proibido desenvolver outras seções sem que eu mencione.
            Veja o exemplo a seguir de uma seção sobre Diagnóstico Diferencial:

            <h2>Diagnóstico Diferencial</h2>
            <div>
            <p>O diagnóstico diferencial da conjuntivite é um passo crucial para assegurar que o tratamento apropriado seja administrado e para evitar complicações decorrentes de diagnósticos incorretos. Dada a variedade de condições oftalmológicas que podem apresentar sintomas semelhantes aos da conjuntivite, é essencial distinguir entre elas com precisão. Segundo Johnson (2019), uma avaliação detalhada do histórico médico do paciente, um exame físico cuidadoso e, quando necessário, exames laboratoriais adicionais são fundamentais para esse processo.</p>

            <p><strong>Conjuntivite Alérgica vs. Outras Alergias Oculares:</strong> A conjuntivite alérgica deve ser diferenciada de outras formas de alergia ocular, como a queratoconjuntivite atópica e a conjuntivite vernal. Ambas podem apresentar sintomas como prurido, lacrimejamento e hiperemia conjuntival, mas tendem a ser mais graves e crônicas. Segundo Miller (2018), a presença de papilas gigantes na conjuntiva tarsal é um indicativo de conjuntivite vernal, enquanto a queratoconjuntivite atópica pode envolver alterações na pele ao redor dos olhos.</p>

            <p><strong>Conjuntivite Viral vs. Conjuntivite Bacteriana:</strong> Diferenciar entre conjuntivite viral e bacteriana é essencial, pois as abordagens terapêuticas são distintas. Segundo Roberts (2020), a conjuntivite viral geralmente apresenta secreção aquosa e sintomas sistêmicos como febre e linfadenopatia pré-auricular, enquanto a conjuntivite bacteriana se caracteriza por secreção purulenta espessa e adesão das pálpebras ao acordar. A história de exposição recente a uma pessoa infectada pode ajudar a sugerir uma etiologia viral.</p>
            </div>

            ---

            Tenha em mente que a seção apresentada anteriormente é apenas um modelo para você seguir. Agora, desenvolva a seção para este titulo: {question}""",
            "Referências": """Crie a referência bibliográfica seguindo esse conteúdo context: {context}"""
        }
