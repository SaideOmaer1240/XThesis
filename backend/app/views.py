
from rest_framework import viewsets, permissions 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import os
from datetime import datetime
from .models import Thesis
from .serializers import ThesisSerializer
from .permissions import IsAuthor 
import re

    
class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = ThesisSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        queryset = Thesis.objects.filter(author=self.request.user).order_by('-date_added')
        
        unique_titles = set()
        unique_queryset = []

        for thesis in queryset:
            if thesis.topic not in unique_titles:
                unique_titles.add(thesis.topic)
                unique_queryset.append(thesis)

        return unique_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ThesisViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    serializer_class = ThesisSerializer

    def get_queryset(self):
        user = self.request.user
        topic_name = self.request.query_params.get('topic_name')
        queryset = Thesis.objects.filter(author=user)
        
        if topic_name:
            queryset = queryset.filter(topic=topic_name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_formatted_text(self, paragraph, text):
        # Expressão regular para encontrar texto entre <h2> e </h2>
        h2_pattern = re.compile(r'<h2>(.*?)</h2>')
        h2_matches = h2_pattern.findall(text)
        
        for i, part  in enumerate(h2_matches):
                if i % 2 == 1:  
                    run = paragraph.add_run(part)
                    run.bold = True
                else:   
                    paragraph.add_run(part)
                    
        # Expressão regular para encontrar texto entre <p> e </p>
        p_pattern = re.compile(r'<p>(.*?)</p>')
        p_matches = p_pattern.findall(text)
        
        for p_match in p_matches:
           
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
           
            run = paragraph.add_run(li_match)
    
    def add_formatted_title(self, paragraph, text):
        parts = text.split('**')
        for i, part in enumerate(parts):
            if i % 2 == 1:
                run = paragraph.add_run(part)
                run.bold = True
            else:
                paragraph.add_run(part)
                
    def add_table(self, doc, text):
        rows = text.strip().split('\n')
        headers = rows[0].split('|')[1:-1]
        
        # Filtrar linhas de cabeçalho de separação
        data = [row.split('|')[1:-1] for row in rows[1:] if '---' not in row]

        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.style = 'Table Grid'
        
        # Add headers
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header.strip()

        # Add data
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            for col_idx, cell_data in enumerate(row_data):
                row_cells[col_idx].text = cell_data.strip()

        # Optional: Add some styling to the table (borders, shading, etc.)
        for cell in table.rows[0].cells:
            cell._element.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="A7BFDE"/>'.format(nsdecls('w'))))

    def variable_content(self, institute, student, instructor, disciplina, topic, cidade):
        year = datetime.now().year
        
        def get_month():
            current_month = datetime.now().month    
            months = {
                1 : 'Janeiro',
                2 : 'Fevereiro',
                3 : 'Março',
                4 : 'Abril',
                5 : 'Maio',
                6 : 'Junho',
                7 : 'Julho',
                8 : 'Agosto',
                9 : 'Setembro',
                10 : 'Outubro',
                11 : 'Novembro',
                12 : 'Dezembro',
            }
            return months.get(current_month)
        
        mes = get_month()
        credentials = {
            'ISaideOmar': institute,
            'CadeiroModuloDisciplina': disciplina,
            'TopicoTema': topic,
            'AutorDiscente': student,
            'SupervisorDocente': instructor,
            'CidadeAutorT': cidade,
            'MesAutorCria': mes,
            'AnoAutorCria': year
        }
        return credentials

    def replace_text(self, doc, replacements):
        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                if key in paragraph.text:
                    inline = paragraph.runs
                    for i in range(len(inline)):
                        if key in inline[i].text:
                            text = inline[i].text.replace(key, str(value))
                            inline[i].text = text
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    self.replace_text(cell, replacements)
    
    @action(detail=False, methods=['get'], url_path='gerar_documento')
    def gerar_documento(self, request):
        user = request.user
        topic_name = request.query_params.get('topic_name')
        
        if not topic_name:
            return Response({'error': 'O parâmetro topic_name é obrigatório.'}, status=400)
        
        
        try:
            # Filtra as teses com base no nome do tópico e pega a primeira tese
            first_thesis = self.get_queryset().filter(topic=topic_name).first()
            # Verifica se a tese existe e imprime o título
            if first_thesis:
                cidade = first_thesis.cidade
                disciplina = first_thesis.disciplina
                institute = first_thesis.institute
                instructor = first_thesis.instructor
                student = first_thesis.student
                
            else:
                cidade='Quelimane',
                disciplina='Quimica',
                institute='Escola Secundária Geral de Quelimane',
                instructor='Antonio',
                student='Saíde Omar Saíde',
        except:
            cidade='Quelimane',
            disciplina='Quimica',
            institute ='Escola Secundária Geral de Quelimane',
            instructor='Antonio',
            student='Saíde Omar Saíde',
            
        theses = self.get_queryset().filter(topic=topic_name)
        if not theses.exists():
            return Response({'error': f'Tópico "{topic_name}" não encontrado.'}, status=404)
        
        doc = Document(os.path.join(settings.MEDIA_ROOT, 'modelo.docx'))
        credentials = self.variable_content(
            cidade=cidade,
            disciplina=disciplina,
            institute=institute,
            instructor=instructor,
            student=student,
            topic=topic_name,
        )
        
        self.replace_text(doc, credentials)
         
        
        for thesis in theses:
             
            self.add_formatted_title(doc.add_paragraph(), f'**{thesis.title}**')
            paragraphs = thesis.text.split('\n\n') 
            for paragraph in paragraphs:
                if '|' in paragraph and '\n' in paragraph:
                    self.add_table(doc, paragraph)
                else:
                    self.add_formatted_text(doc.add_paragraph(), paragraph)
        
        directory = os.path.join(settings.MEDIA_ROOT, 'documents')
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_name = f'{topic_name}.docx'
        file_path = os.path.join(directory, file_name)
        doc.save(file_path)
        
        file_url = os.path.join(settings.MEDIA_URL, 'documents', file_name)
        return Response({'file_url': file_url})
