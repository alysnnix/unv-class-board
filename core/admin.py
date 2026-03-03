from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib import admin
from django.conf import settings
from datetime import datetime
import os
import locale

from .models import Teacher, Justification, SchoolSegment, ClassGroup, SchoolPeriod, Subject

# --- Set locale for dates ---
try:
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
except locale.Error:
    pass

def generate_pdf_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    date_str = datetime.now().strftime("%B %d, %Y")
    canvas.setFont('Helvetica-Oblique', 8)
    canvas.drawString(2 * cm, 1.5 * cm, f"Issue Date: {date_str}")

    username = getattr(doc, 'username', '')
    if username:
        canvas.drawRightString(width - 2 * cm, 1.5 * cm, f"Issued by: {username}")
    canvas.restoreState()

def export_model_to_pdf(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    fields = [field.name for field in meta.fields if field.name != 'id']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{meta.verbose_name_plural}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=3*cm, rightMargin=3*cm, topMargin=3*cm, bottomMargin=3*cm)
    elements = []

    logo_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'logo-painel_interativo.jpeg')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=3.5*cm, height=2*cm)
    else:
        img = Spacer(3.5*cm, 2*cm)

    title = Paragraph(
        f'<b><font size=14 color=blue>{meta.verbose_name_plural.title()}</font></b>',
        ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, fontSize=14)
    )

    header = Table([[img, title]], colWidths=[4*cm, 12*cm])
    header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(header)
    elements.append(Spacer(1, 12))

    total_records = queryset.count()
    style_qty = ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=10)
    qty_paragraph = Paragraph(f"<b>Total Records: {total_records}</b>", style_qty)
    elements.append(qty_paragraph)
    elements.append(Spacer(1, 12))

    data = [[field.replace('_', ' ').title() for field in fields]]
    for obj in queryset:
        row = [str(getattr(obj, field)) for field in fields]
        data.append(row)

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)

    user = request.user
    doc.username = user.get_full_name() or user.username if user.is_authenticated else ""

    doc.build(elements, onFirstPage=generate_pdf_footer, onLaterPages=generate_pdf_footer)
    return response

export_model_to_pdf.short_description = "Export to PDF"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_substitute_formatted')
    actions = [export_model_to_pdf]

    def is_substitute_formatted(self, obj):
        return "Yes" if obj.is_substitute else "No"
    is_substitute_formatted.short_description = "Substitute"

@admin.register(Justification)
class JustificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_model_to_pdf]

@admin.register(SchoolSegment)
class SchoolSegmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_model_to_pdf]

@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'segment', 'period')
    actions = [export_model_to_pdf]

@admin.register(SchoolPeriod)
class SchoolPeriodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_model_to_pdf]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_model_to_pdf]