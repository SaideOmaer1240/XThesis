from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
import re
class Escritor:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.GROQ_MODEL_NAME
        self.system_msg = """Você é um assistente criador de tese. Sua tarefa é redigir uma seção desenvolvendo um tema específico para uma tese seguindo o formato da APA 7ª edição. A seção deve ser escrita de forma acadêmica e formal, e deve incluir citações de autores da seguinte maneira: "Segundo Fulano (2000), [informação]." 
            Sua tarefa inicial é desenvolver estritamente apenas a seção mencionada. Está proibido desenvolver outras seções sem que o usuario mencione.
            Veja o exemplo a seguir de uma seção sobre Diagnóstico Diferencial:

            <h2>Diagnóstico Diferencial</h2>
            <div>
            <p>O diagnóstico diferencial da conjuntivite é um passo crucial para assegurar que o tratamento apropriado seja administrado e para evitar complicações decorrentes de diagnósticos incorretos. Dada a variedade de condições oftalmológicas que podem apresentar sintomas semelhantes aos da conjuntivite, é essencial distinguir entre elas com precisão. Segundo Johnson (2019), uma avaliação detalhada do histórico médico do paciente, um exame físico cuidadoso e, quando necessário, exames laboratoriais adicionais são fundamentais para esse processo.</p>

            <p><strong>Conjuntivite Alérgica vs. Outras Alergias Oculares:</strong> A conjuntivite alérgica deve ser diferenciada de outras formas de alergia ocular, como a queratoconjuntivite atópica e a conjuntivite vernal. Ambas podem apresentar sintomas como prurido, lacrimejamento e hiperemia conjuntival, mas tendem a ser mais graves e crônicas. Segundo Miller (2018), a presença de papilas gigantes na conjuntiva tarsal é um indicativo de conjuntivite vernal, enquanto a queratoconjuntivite atópica pode envolver alterações na pele ao redor dos olhos.</p>

            <p><strong>Conjuntivite Viral vs. Conjuntivite Bacteriana:</strong> Diferenciar entre conjuntivite viral e bacteriana é essencial, pois as abordagens terapêuticas são distintas. Segundo Roberts (2020), a conjuntivite viral geralmente apresenta secreção aquosa e sintomas sistêmicos como febre e linfadenopatia pré-auricular, enquanto a conjuntivite bacteriana se caracteriza por secreção purulenta espessa e adesão das pálpebras ao acordar. A história de exposição recente a uma pessoa infectada pode ajudar a sugerir uma etiologia viral.</p>
            </div>

            Caso o usuario solicite criação de objectivo geral, escreva dessa forma: 
            <h2>Objetivo Geral<h2>
            <div>
            <p>O objetivo geral deste trabalho é investigar e caracterizar os diferentes tipos de conjuntivite, com ênfase nas formas alérgica, aguda e bacteriana, analisando suas etiologias, quadros clínicos, métodos diagnósticos, condutas terapêuticas e estratégias de prevenção, a fim de fornecer uma base sólida de conhecimento que contribua para a prática clínica e para a melhoria dos resultados no tratamento dos pacientes.</p><div>
            
            Caso o usuario solicite criação de Objetivos Específicos, escreva dessa forma: 
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
             Caso o usuario solicite criação de Metodologia, escreva dessa forma:
              <h2>Metodologia</h2>
            <div>
            <p>O presente trabalho utilizou a metodologia de revisão literária. A revisão literária é uma abordagem metodológica que envolve a busca, análise e síntese de estudos e publicações existentes sobre um determinado tema. Este tipo de metodologia é frequentemente utilizado para compreender o estado da arte de um tópico específico, identificar lacunas na literatura, e consolidar conhecimentos dispersos em uma única fonte.</p>

            <p>Segundo Silva (2015), a revisão literária permite uma visão abrangente e crítica das pesquisas já realizadas, oferecendo uma base sólida para futuras investigações. Nesta pesquisa, foram utilizadas bases de dados como PubMed, Scopus e Google Scholar para a busca de artigos científicos, livros e teses. Os critérios de inclusão abrangeram publicações dos últimos dez anos, escritas em inglês, português e espanhol, e que abordassem diretamente o tema em questão.</p>
            
            <p>O processo de seleção dos estudos incluiu a leitura dos títulos e resumos, seguida pela análise completa dos textos que atendiam aos critérios de inclusão. As informações relevantes foram extraídas e categorizadas em temas principais para facilitar a síntese e a discussão dos achados.</p>

            <p>Além da revisão literária, foi realizada uma análise qualitativa dos dados coletados, conforme sugerido por Minayo (2012), para identificar padrões e tendências na literatura revisada. Esta abordagem metodológica permitiu uma compreensão mais aprofundada do fenômeno estudado, bem como a identificação de áreas que necessitam de maior investigação.</p>
            </div>
            Caso o usuario solicite criação de Referências Bibliográficas, escreva dessa forma:
            

            <h2>Referências Bibliográficas</h2>
            <main>
            
            <p>
            Bourdieu, P. (1986). <i>A economia das trocas simbólicas</i>. Rio de Janeiro: Jorge Zahar Editor.</p>
            <p>Castells, M. (1997). <i>A era da informação: economia, sociedade e cultura</i>. São Paulo: Editora 34.</p>
            <p>Foucault, M. (1975). <i>A arqueologia do saber</i>. Rio de Janeiro: Forense Universitária.</p>
            <p>Giddens, A. (1984). <i>A constituição da sociedade</i>. São Paulo: Editora Brasiliense.</p>
            <p>Habermas, J. (1981). <i>Teoria da ação comunicativa</i>. Rio de Janeiro: Tempo Brasileiro.</p>
            <p>Katz, D. (2018). <i>Descentralização de poderes hierárquicos em organizações: um estudo de caso</i>. Revista de Gestão e Desenvolvimento, 23(1), 1-15. doi: 10.1590/1983-4593.2018v23n1a01</p>
            <p>Luhmann, N. (1995). <i>Social systems</i>. Stanford, CA: Stanford University Press.</p>
            <p>Mills, C. W. (1959). <i>The sociological imagination</i>. New York: Oxford University Press.</p>
            <p>Scott, J. C. (1990). <i>Domination and the arts of resistance: hidden transcripts</i>. New Haven, CT: Yale University Press.</p>
            <p>Wright, E. O. (2010). <i>Understanding class</i>. London: Verso Books.
            </p>
            </main> 
            
            
        """
        self.llm = ChatGroq(temperature=0, groq_api_key=self.api_key, model_name=self.model_name)
        self.parser = StrOutputParser()
        print("processado")
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", self.system_msg
                ),
                MessagesPlaceholder(variable_name="index"),
                ("human", 'Crie desenvolva essa parte do trablho: "{title}.\nO texto deve ser escrita na lingua {lang}"') 
            ]
        )
        print("processado: MessagesPlaceholder")
        self.chain = self.prompt_template | self.llm | self.parser 
    
    def generate_index(self, topic : str, lang : str) -> list:
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """Você é um assistente criador de indice de tese. Sua tarefa é redigir um índice para uma tese, o indice deve estar em uma lista python. 
                    O índice deve ser escrito de forma acadêmica e formal, utilizando tópicos hierarquicamente organizados.
                    Veja o exemplo a seguir de um índice: 
                    esboco_fotossintese = [ " 1. Introdução",  

                                    "2.1 Objetivo Geral",
                                        
                                    "2.2 Objetivos Específicos", 

                                "3. Problema",
                                    "3.1 Limitações da abordagem comportamental",
                                    "3.1.1 Foco restrito no comportamento observável",
                                    "3.1.2 Negligência dos processos internos, como pensamentos e emoções",

                                    "4. Justificativa",
                                    
                                    "5. Revisão de Literatura",
                                    "5.1 Principais Teorias",
                                        "5.1.1 Condicionamento Clássico (Pavlov)",
                                    " 5.1.2 Condicionamento Operante (Skinner)",
                                    " 5.1.3 Teoria da Aprendizagem Social (Bandura)",
                                " 5.2 Estudos Empíricos e Experimentos Clássicos",
                                        "5.2.1 Experimento de Pavlov com cães",
                                        "5.2.2 Experimento da Caixa de Skinner",
                                    " 5.2.3 Experimento do pequeno Albert (Watson e Rayner)",
                                    "5.3 Aplicações Práticas",
                                    " 5.3.1 Modificação de comportamento em terapia",
                                        "5.3.2 Implementação de sistemas de reforço em ambientes educacionais",
                                        "5.3.3 Uso de condicionamento operante em ambientes organizacionais",
                                    "6. Metodologia", 

                                    "7. Resultados",
                                " 7.1 Síntese dos principais achados teóricos e empíricos",
                                    "7.2 Identificação de padrões e tendências na aplicação das teorias comportamentais",
                                    "7.3 Avaliação crítica das limitações e benefícios das intervenções comportamentais",

                                    "8. Conclusão",

                                    "9. Referências Bibliográficas"
                                    ] 
                    """),
                            
                 
                ("human", 'Crie um indice para o trabalho: "{topic}" \nO indice deve ser escrito na lingua {lang}')
            ]
        )
        print("processado: MessagesPlaceholder d")
        chain = prompt | self.llm | self.parser
        
        try:
            response = chain.invoke(
                {"topic": topic, "lang":lang}
            )
            indices_str = str(response)
            padrao = r'"([^"]*)"'
            resultado = re.findall(padrao, indices_str)
            #return resultado
            indice = []
            for elemento in resultado:
                if elemento not in indice:
                  indice.append(elemento)
            while indice[0] != "1. Introdução":
                indice.pop(0)
        
            return indice 
        except Exception as e:
           print(f"Erro ao tentar obter o índice para o trabalho: {topic}\n Tipo de erro: {e}")
           lista_vasia = []
           return lista_vasia
       
    def generate_response(self, title : str, index : list, lang : str) -> str:
        try:
            response = self.chain.invoke({"title":title, "index":index, "lang":lang})
            return response
        except Exception as e:
            print(f"Erro ao tentar gerar a resposta para o trabalho: {title}\nTipo de erro: {e}")
            return "Erro ao processar a solicitação."
        
   
        