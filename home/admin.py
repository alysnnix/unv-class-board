from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from datetime import datetime
import os
import locale
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from .models import Professor, Justificativa, Segmento, Turma, \
    Periodo, Componente_Curricular

# --- Define locale para datas em português ---
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/Mac
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  # Windows
    except locale.Error:
        pass  # Fallback to default locale

# --- Função para rodapé com data e nome do usuário ---
def rodape(canvas, doc):
    canvas.saveState()
    largura, altura = A4

    data_str = datetime.now().strftime("%d de %B de %Y")
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawString(2 * cm, 1.5 * cm, f"Data de emissão: {data_str}")

    nome_usuario = getattr(doc, 'nome_usuario', '')
    if nome_usuario:
        canvas.drawRightString(largura - 2 * cm, 1.5 * cm, f"Emitido por: {nome_usuario}")

    canvas.restoreState()

# --- Função para exportar PDF ---
def exportar_modelo_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    campos = [field.name for field in meta.fields if field.name != 'id']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name_plural}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            leftMargin=3*cm, rightMargin=3*cm,
                            topMargin=3*cm, bottomMargin=3*cm)

    elementos = []

    # --- Cabeçalho com logo e título centralizado ---
    caminho_logo = os.path.join(settings.BASE_DIR, 'home', 'static', 'logo-painel_interativo.jpeg')
    styles = getSampleStyleSheet()

    if os.path.exists(caminho_logo):
        img = Image(caminho_logo, width=3.5*cm, height=2*cm)
    else:
        img = Spacer(3.5*cm, 2*cm)  # Espaço reservado

    titulo = Paragraph(
        f'<b><font size=14 color=blue>{meta.verbose_name_plural.title()}</font></b>',
        ParagraphStyle(name='TituloCentral', alignment=TA_CENTER, fontSize=14)
    )

    cabecalho = Table(
        [[img, titulo]],
        colWidths=[4*cm, 12*cm]
    )
    cabecalho.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elementos.append(cabecalho)
    elementos.append(Spacer(1, 12))

    # --- Quantidade de registros ---
    total_registros = queryset.count()
    estilo_qtd = ParagraphStyle(name='Centro', alignment=TA_CENTER, fontSize=10)
    qtd_paragraph = Paragraph(f"<b>Quantidade de registros: {total_registros}</b>", estilo_qtd)
    elementos.append(qtd_paragraph)
    elementos.append(Spacer(1, 12))

    # --- Tabela de dados ---
    dados = [[campo.title() for campo in campos]]
    for obj in queryset:
        linha = [str(getattr(obj, campo)) for campo in campos]
        dados.append(linha)

    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabela)

    # --- Nome do usuário autenticado ---
    usuario = request.user
    nome_usuario = usuario.get_full_name() or usuario.username if usuario.is_authenticated else ""
    doc.nome_usuario = nome_usuario

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)

    return response

exportar_modelo_pdf.short_description = "Exportar como PDF"

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome','telefone','componente_curricular','substituto_formatado')
    actions = [exportar_modelo_pdf]

    def substituto_formatado(self, obj):
        return "Sim" if obj.substituto else "Não"

    substituto_formatado.short_description = "Substituto"

@admin.register(Justificativa)
class JustificativaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome','segmento','periodo')
    actions = [exportar_modelo_pdf]

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

@admin.register(Componente_Curricular)
class Componente_CurricularAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    actions = [exportar_modelo_pdf]

    