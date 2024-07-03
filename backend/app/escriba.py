import os
import time
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings
class Esboco:
    def indice(self):
        return ["introdução", "objetivo geral", "objetivo especifico", "metodologia", "justificativa"]
    

    def conclusao(self):
        return ["Conclusão", "Bibliografia"]
class Escriba:
    def __init__(self):
        groq_api_key = settings.GROQ_API_KEY
        self.llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")

    def resposta_em_json(self, indices):
        indices_str = str(indices)
        padrao = r'"([^"]*)"'
        resultado = re.findall(padrao, indices_str)
        return resultado

    def escreva(self, tema):
        print('Tema:', tema)
        respostas = []
        introduzir = """Imagine-se redigindo um trabalho escolar sobre um tema crucial: ["{question}"]. Para criar uma introdução impactante para este trabalho, siga estas orientações essenciais: Inicie com uma afirmação marcante: Abra sua introdução com uma frase impactante que instantaneamente prenda a atenção do leitor em relação ao tema. Contextualize o tema: Posteriormente, ofereça uma breve descrição do tema, utilizando estatísticas pertinentes ou exemplos concretos para ilustrar a magnitude do problema ou a importância. Exponha a estrutura do trabalho: Conclua sua introdução delineando sucintamente a organização do trabalho. Nota: No ensaio substitua o termo 'ensaio' por 'Trabalho'. E também não precisa adicionar subtítulo."""
        objectivo_geral = """Elabore um objetivo geral do tema "{question}": \n Nota: Não adicione subtítulo, apenas apresente o objetivo geral"""
        objectivos_especifico = """Elabore os objetivos específicos para "{question}": \n Nota: Não adicione subtítulo, apenas apresente os objetivos específicos"""
        metodologia = """Apresente qual metodologia usará para elaborar o trabalho sobre "{question}": \n Use citação de autor seguindo as normas APA para credibilizar suas afirmações na escolha da metodologia. A citação deve ter esse formato. Exemplo: Para Mourão & Mark (2001), Como a chama terna de uma vela, era assim que eu via pessoas, animais, geografias várias, (p. 10). """
        justificativa = """Elabore uma justificativa do tema "{question}": Explique o interesse ou a curiosidade que despertou essa escolha; """
        bibliografia = """Crie a referência bibliográfica seguindo esse conteúdo context: {context} """

        prompt_template = """
        Desenvolva um esboço detalhado, criando um índice ou sumário para o trabalho sobre {question}.
        O esboço deve estar em formato de json. A resposta sua deve ser absolutamente apenas o conteúdo em json, não retorne outro tipo de conteúdo antes ou depois de json. As chaves devem ter aspas simples e os valores aspas duplas, por exemplo: 'Título': "Fotossíntese das Plantas".
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        model = self.llm
        outline_chain = (
            prompt
            | model
            | StrOutputParser()
        )

        indices = outline_chain.invoke({"question": tema})
        sumario = self.resposta_em_json(indices)

        indice = Esboco.indice(self)
        conclusao = Esboco.conclusao(self)
        for elemento in sumario:
            indice.append(elemento)
        for i in conclusao:
            indice.append(i)

        sumario_completo = ' '.join(sumario)
        desenvolver = sumario_completo + """: \n Elaborar um trabalho acadêmico seguindo rigorosamente as diretrizes da APA (American Psychological Association) sobre o tema {question}. Cada argumento apresentado deve ser apoiado em ideias de autores renomados na área. Garanta a utilização de referências bibliográficas confiáveis para fundamentar suas análises e argumentos. A citação do autor no texto deverá seguir o formato APA, seguindo este exemplo de citação: 'Segundo Silva (2019), a aprendizagem é potencializada pela interação social, pois os alunos se beneficiam da troca de conhecimentos, ideias e experiências entre si. Essa interação permite que os alunos explorem diferentes perspectivas, reflitam criticamente sobre o conteúdo e construam seu próprio conhecimento (p. 23-24). Segundo Silva & Santos (2019), a interação social é fundamental para o processo de aprendizagem. O trabalho deve conter um desenvolvimento consistente e uma conclusão que sintetize as principais ideias abordadas. Não escreva o título ou subtítulo."""

        linha_de_saida_introducao = ChatPromptTemplate.from_template(introduzir)
        linha_de_saida_obj_geral = ChatPromptTemplate.from_template(objectivo_geral)
        linha_de_saida_obj_especifico = ChatPromptTemplate.from_template(objectivos_especifico)
        linha_de_saida_metodologia = ChatPromptTemplate.from_template(metodologia)
        linha_de_saida_justificativa = ChatPromptTemplate.from_template(justificativa)
        linha_de_saida_bibliografia = ChatPromptTemplate.from_template(bibliografia)
        linha_de_saida = ChatPromptTemplate.from_template(desenvolver)

        for titulo in indice:
            if "introdução" in titulo:
                chain1 = (
                    linha_de_saida_introducao
                    | model
                    | StrOutputParser()
                )
                resposta = chain1.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': resposta})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "objetivo geral" in titulo:
                chain2 = (
                    linha_de_saida_obj_geral
                    | model
                    | StrOutputParser()
                )
                resposta = chain2.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': resposta})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "objetivo específico" in titulo:
                chain3 = (
                    linha_de_saida_obj_especifico
                    | model
                    | StrOutputParser()
                )
                texto = chain3.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': texto})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "metodologia" in titulo:
                chain4 = (
                    linha_de_saida_metodologia
                    | model
                    | StrOutputParser()
                )
                texto = chain4.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': texto})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "justificativa" in titulo:
                chain5 = (
                    linha_de_saida_justificativa
                    | model
                    | StrOutputParser()
                )
                texto = chain5.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': texto})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif titulo:
                chain6 = (
                    linha_de_saida
                    | model
                    | StrOutputParser()
                )
                texto = chain6.invoke({"question": titulo})
                respostas.append({'title': titulo, 'text': texto})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "Conclusão" in titulo:
                resposta = chain6.invoke({"question": tema})
                respostas.append({'title': titulo, 'text': resposta})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
            elif "Referências bibliográficas" in titulo:
                chain7 = (
                    linha_de_saida_bibliografia
                    | model
                    | StrOutputParser()
                )
                resposta = chain7.invoke({"context": "conteúdo de exemplo"})
                respostas.append({'title': titulo, 'text': resposta})
                print(f"{titulo} concluído com sucesso")
                time.sleep(30)
        return respostas
