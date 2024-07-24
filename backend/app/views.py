from rest_framework import viewsets, permissions
from rest_framework.generics import DestroyAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from docx import Document
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import os  
from .models import Thesis
from .serializers import ThesisSerializer
from .permissions import IsAuthor
from accounts.datetime import DateTime
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

    def copiar_estilos(self, origem, destino):
        destino.style = origem.style
        destino.paragraph_format.alignment = origem.paragraph_format.alignment
        destino.paragraph_format.left_indent = origem.paragraph_format.left_indent
        destino.paragraph_format.right_indent = origem.paragraph_format.right_indent
        destino.paragraph_format.first_line_indent = origem.paragraph_format.first_line_indent
        destino.paragraph_format.keep_together = origem.paragraph_format.keep_together
        destino.paragraph_format.keep_with_next = origem.paragraph_format.keep_with_next
        destino.paragraph_format.page_break_before = origem.paragraph_format.page_break_before
        destino.paragraph_format.widow_control = origem.paragraph_format.widow_control
        destino.paragraph_format.space_before = origem.paragraph_format.space_before
        destino.paragraph_format.space_after = origem.paragraph_format.space_after
        destino.paragraph_format.line_spacing = origem.paragraph_format.line_spacing
        destino.paragraph_format.line_spacing_rule = origem.paragraph_format.line_spacing_rule

    def localizar_paragrafo(self, document, texto):
        for paragraph in document.paragraphs:
            if texto in paragraph.text:
                return paragraph
        return None
    
    def remover_paragrafo(self, doc, paragrafo):
        p = paragrafo._element
        p.getparent().remove(p)
        p._element = p._p = None

    def add_formatted_text(self, paragraph, text):
        def apply_formatting(part, bold=False, italic=False):
            run = paragraph.add_run(part)
            run.bold = bold
            run.italic = italic

         # Procura por <h2>
        h2_pattern = re.compile(r'<h2>(.*?)</h2>')
        h2_matches = h2_pattern.findall(text)
        for i, part in enumerate(h2_matches):
            apply_formatting(part, bold=True if i % 2 == 1 else False)

        # Procura por <p>
        p_pattern = re.compile(r'<p>(.*?)</p>')
        p_matches = p_pattern.findall(text)
        for p_match in p_matches:
            # Primeira iteração: procura por <strong>
            strong_pattern = re.compile(r'<strong>(.*?)</strong>')
            parts = strong_pattern.split(p_match)
            for i, part in enumerate(parts):
                # Segunda iteração: procura por <i> dentro das partes encontradas por <strong>
                italic_pattern = re.compile(r'<i>(.*?)</i>')
                italic_parts = italic_pattern.split(part)
                for j, italic_part in enumerate(italic_parts):
                    apply_formatting(italic_part, bold=False if i % 2 == 1 else False, italic=True if j % 2 == 1 else False)
 

        li_pattern = re.compile(r'<li>(.*?)</li>')
        li_matches = li_pattern.findall(text)
        for li_match in li_matches:
            apply_formatting(li_match)

    def add_table(self, doc, text):
        rows = text.strip().split('\n')
        headers = rows[0].split('|')[1:-1]
        
        data = [row.split('|')[1:-1] for row in rows[1:] if '---' not in row]

        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.style = 'Table Grid'
        
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header.strip()

        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            for col_idx, cell_data in row_data:
                row_cells[col_idx].text = cell_data.strip()

        for cell in table.rows[0].cells:
            cell._element.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="A7BFDE"/>'.format(nsdecls('w'))))

    def variable_content(self, institute, student, instructor, disciplina, topic, cidade):
        year = DateTime.year()
        mes = DateTime.get_month()
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
        def replace_in_paragraph(paragraph):
            for key, value in replacements.items():
                if key in paragraph.text:
                    inline = paragraph.runs
                    for i in range(len(inline)):
                        if key in inline[i].text:
                            inline[i].text = inline[i].text.replace(key, str(value))
        
        for paragraph in doc.paragraphs:
            replace_in_paragraph(paragraph)

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
        
        first_thesis = self.get_queryset().filter(topic=topic_name).first()
        
        if first_thesis:
            cidade = first_thesis.cidade
            disciplina = first_thesis.disciplina
            institute = first_thesis.institute
            instructor = first_thesis.instructor
            student = first_thesis.student
        else:
            cidade = 'Quelimane'
            disciplina = 'Quimica'
            institute = 'Escola Secundária Geral de Quelimane'
            instructor = 'Antonio'
            student = 'Saíde Omar Saíde'
            
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
            paragrafo_origem = self.localizar_paragrafo(doc, 'Copiar parágrafo')
            if paragrafo_origem:
                paragrafo_destino = doc.add_paragraph()
                self.copiar_estilos(paragrafo_origem, paragrafo_destino)
                paragrafo_destino.text = thesis.title
            else:
                self.add_formatted_text(doc.add_paragraph(), f'**{thesis.title}**')
                
            paragraphs = thesis.text.split('\n\n')
            for paragraph in paragraphs:
                if '|' in paragraph and '\n' in paragraph:
                    self.add_table(doc, paragraph)
                else:
                    self.add_formatted_text(doc.add_paragraph(), paragraph)
        
        self.remover_paragrafo(doc, paragrafo_origem)
        directory = os.path.join(settings.MEDIA_ROOT, 'documents/', user.username)
        
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.docx'):
                        dir_file = os.path.join(root, file)
                        os.remove(dir_file)                
        else:
            os.makedirs(directory)
            
        
        file_name = f'{topic_name}.docx'
        file_path = os.path.join(directory, file_name)
        doc.save(file_path)
         
        with open(file_path, 'rb') as arquivo_aberto:
            response = HttpResponse(
                arquivo_aberto.read(), 
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
             
            return response
    
     
        

class DestroyAllTheses(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    queryset = Thesis.objects.all()
    
    def get_object(self): 
        user = self.request.user
        return Thesis.objects.filter(author=user)

class DestroyOneThesis(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    
    
    def get_object(self):
        user = self.request.user
        topic_name = self.request.query_params.get('topic_name')
        queryset = Thesis.objects.filter(author=user)
        
        if topic_name:
            queryset = queryset.filter(topic=topic_name)
            return queryset
    