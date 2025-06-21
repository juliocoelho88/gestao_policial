from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Policial, Producao
from django.http import HttpResponse
import csv
import os

@admin.register(Policial)
class PolicialAdmin(admin.ModelAdmin):
    list_display = ('nome_guerra', 'graduacao', 're', 'pelotao')
    search_fields = ('nome_guerra', 're')

@admin.register(Producao)
class ProducaoAdmin(admin.ModelAdmin):
    list_display = ('policial', 'data', 'pessoa', 'carros', 'motos', 'pontuacao')
    list_filter = (
        ('data', DateFieldListFilter),
        'policial__pelotao',
    )
    search_fields = ('policial__nome_guerra', 'policial__re')
    actions = ['exportar_csv', 'exportar_excel']


    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="producao.csv"'
        writer = csv.writer(response)

        campos = [
            'data', 'nome_guerra', 're', 'pelotao',
            'pessoa', 'pessoas_aisp', 'carros', 'carros_aisp',
            'motos', 'motos_aisp', 'qnt_ocorrencias', 'flagrantes',
            'flagrantes_aisp', 'autuacoes', 'raia', 'procurado',
            'carro_apreendido', 'moto_apreendida', 'flagrantes_outros',
            'arma', 'escolas', 'pontuacao'
        ]

        writer.writerow(campos)

        for p in queryset:
            writer.writerow([
                p.data, p.policial.nome_guerra, p.policial.re, p.policial.pelotao,
                p.pessoa, p.pessoas_aisp, p.carros, p.carros_aisp,
                p.motos, p.motos_aisp, p.qnt_ocorrencias, p.flagrantes,
                p.flagrantes_aisp, p.autuacoes, p.raia, p.procurado,
                p.carro_apreendido, p.moto_apreendida, p.flagrantes_outros,
                p.arma, p.escolas, p.pontuacao
            ])

        return response

    def exportar_excel(self, request, queryset):
        # ... criação da planilha
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active

        headers = ['data', 'nome_guerra', 're', 'pelotao', 'pessoa', 'pessoa_aisp', 'carros', 'carros_aisp', 'motos',
                   'motos_aisp',
                   'qnt_ocorrencias', 'flagrantes', 'flagrantes_aisp', 'autuacoes', 'raia', 'procurado',
                   'carro_apreendido', 'moto_apreendida', 'flagrantes_outros', 'arma', 'escolas', 'pontuacao']
        ws.append(headers)

        for p in queryset:
            ws.append([
                p.data.strftime('%Y-%m-%d'),
                p.policial.nome_guerra,
                p.policial.re,
                p.policial.pelotao,
                p.pessoa, p.pessoas_aisp, p.carros, p.carros_aisp,
                p.motos, p.motos_aisp, p.qnt_ocorrencias, p.flagrantes,
                p.flagrantes_aisp, p.autuacoes, p.raia, p.procurado,
                p.carro_apreendido, p.moto_apreendida, p.flagrantes_outros,
                p.arma, p.escolas, p.pontuacao
            ])

        # Caminho local (pode ser uma pasta da rede, como \\192.168.0.100\relatorios)
        pasta_exportacao = r'C:\relatorios\producoes'  # ou um caminho de rede local
        os.makedirs(pasta_exportacao, exist_ok=True)

        from datetime import datetime
        nome_arquivo = f"producao_{datetime.now().strftime('%Y-%m-%d_%Hh%Mm')}.xlsx"
        caminho_completo = os.path.join(pasta_exportacao, nome_arquivo)

        wb.save(caminho_completo)

        # Também envia como download
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
        wb.save(response)
        return response

    exportar_csv.short_description = "Exportar como CSV"
    exportar_excel.short_description = "Exportar como Excel"
