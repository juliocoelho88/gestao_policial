import os
import shutil
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import EquipeProdutividade  # ajuste se o nome do app for diferente
from datetime import datetime, timedelta

# 🔹 Tabela de pesos (regras de negócio)
PONTOS = {
        'pessoa': 0.01,
        'pessoas_aisp': 0.1,
        'carros': 0.01,
        'carros_aisp': 0.1,
        'motos': 0.01,
        'motos_aisp': 0.1,
        'qnt_ocorrencias': 0.01,
        'flagrantes': 2,
        'flagrantes_aisp': 3,
        'autuacoes': 0.05,
        'raia': 0.05,
        'procurado': 1,
        'carro_apreendido': 0.2,
        'moto_apreendida': 0.2,
        'flagrantes_outros': 0.5,
        'arma': 1,
        'escolas': 0.01,
    }

class Command(BaseCommand):
    help = 'Exporta dados de produtividade (com pontos) para CSV (local + Google Drive) e mantém apenas últimos 30 dias'

    def handle(self, *args, **kwargs):
        agora = datetime.now()
        data = agora.strftime("%Y-%m-%d_%H-%M")
        mes = agora.strftime("%Y-%m")  # Ex: 2025-09

        # --- 📂 Pasta local ---
        pasta_local = os.path.join(settings.BASE_DIR, 'exportacoes')
        os.makedirs(pasta_local, exist_ok=True)

        # --- 📂 Pasta Google Drive ---
        pasta_drive_base = r"G:\Meu Drive\PowerBI\Exportacoes"
        pasta_drive_mes = os.path.join(pasta_drive_base, mes)
        os.makedirs(pasta_drive_mes, exist_ok=True)

        # --- Buscar dados no banco ---
        dados_prod = EquipeProdutividade.objects.all().values()
        df = pd.DataFrame(dados_prod)

        # --- Calcular pontos ---
        df['pontos'] = 0
        for coluna, peso in PONTOS.items():
            if coluna in df.columns:
                df['pontos'] += df[coluna] * peso

        # --- Exportar CSV (local) ---
        arquivo_local = os.path.join(pasta_local, f"produtividade_{data}.csv")
        df.to_csv(arquivo_local, index=False, encoding='utf-8-sig')
        self.stdout.write(self.style.SUCCESS(f"Exportação criada: {arquivo_local}"))

        # --- Copiar para Google Drive ---
        arquivo_drive = os.path.join(pasta_drive_mes, f"produtividade_{data}.csv")
        shutil.copy2(arquivo_local, arquivo_drive)
        self.stdout.write(self.style.SUCCESS(f"Exportação copiada para Drive: {arquivo_drive}"))

        # --- 🧹 Limpeza automática (30 dias) ---
        limite = agora - timedelta(days=30)

        def limpar_pasta(pasta):
            for root, dirs, files in os.walk(pasta):
                for f in files:
                    if f.startswith("produtividade_") and f.endswith(".csv"):
                        caminho = os.path.join(root, f)
                        try:
                            data_str = f.replace("produtividade_", "").replace(".csv", "")
                            dt_arquivo = datetime.strptime(data_str, "%Y-%m-%d_%H-%M")
                            if dt_arquivo < limite:
                                os.remove(caminho)
                                self.stdout.write(self.style.WARNING(f"Exportação antiga removida: {caminho}"))
                        except Exception:
                            pass  # ignora arquivos fora do padrão

        limpar_pasta(pasta_local)
        limpar_pasta(pasta_drive_base)




