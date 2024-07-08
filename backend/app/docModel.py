
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
# Função para copiar estilos de um parágrafo para outro




# Função para adicionar um campo de sumário automático
def adicionar_sumario(doc):
    # Cria o parágrafo onde o sumário será inserido
    paragrafo_sumario = doc.add_paragraph()
    
    # Cria o campo para o sumário
    run = paragrafo_sumario.add_run()
    fld_char = OxmlElement('w:fldChar')
    fld_char.set(qn('w:fldCharType'), 'begin')
    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = 'TOC \\o "1-3" \\h \\z \\u'
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'separate')
    fld_char3 = OxmlElement('w:fldChar')
    fld_char3.set(qn('w:fldCharType'), 'end')
    
    run._r.append(fld_char)
    run._r.append(instr_text)
    run._r.append(fld_char2)
    run._r.append(fld_char3)