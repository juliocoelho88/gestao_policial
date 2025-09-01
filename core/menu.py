from django.db import models

class RankingPlaceholder(models.Model):
    class Meta:
        verbose_name = "📊 Ver Ranking"
        verbose_name_plural = "📊 Ver Ranking"
        managed = False

class ExportacaoPlaceholder(models.Model):
    class Meta:
        verbose_name = "📤 Exportar Dados"
        verbose_name_plural = "📤 Exportar Dados"
        managed = False