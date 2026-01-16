import os
import shutil
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.conf import settings

class Command(BaseCommand):
    help = 'Cria backup do banco SQLite, copia para o Google Drive e mantém apenas os últimos 30 dias'

    def handle(self, *args, **kwargs):
        # Caminho do banco
        db_path = settings.DATABASES['default']['NAME']

        # Data formatada
        agora = datetime.now()
        data = agora.strftime("%Y-%m-%d_%H-%M")
        mes = agora.strftime("%Y-%m")  # Ex: 2025-09
        nome_backup = f"backup_{data}.sqlite3"

        # --- 📂 Pasta local ---
        pasta_backup_local = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(pasta_backup_local, exist_ok=True)
        destino_local = os.path.join(pasta_backup_local, nome_backup)

        # Cria o backup local
        shutil.copy2(db_path, destino_local)
        self.stdout.write(self.style.SUCCESS(f"Backup local criado em: {destino_local}"))

        # --- 📂 Pasta do Google Drive (organizada por mês) ---
        pasta_drive_base = r"G:\Meu Drive\Backups"
        pasta_drive_mes = os.path.join(pasta_drive_base, mes)
        os.makedirs(pasta_drive_mes, exist_ok=True)

        destino_drive = os.path.join(pasta_drive_mes, nome_backup)

        try:
            shutil.copy2(destino_local, destino_drive)
            self.stdout.write(self.style.SUCCESS(f"Backup também copiado para o Google Drive: {destino_drive}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Falha ao copiar para o Google Drive: {e}"))

        # --- 🧹 Limpeza automática (30 dias) ---
        limite = agora - timedelta(days=30)

        def limpar_pasta(pasta):
            for root, dirs, files in os.walk(pasta):
                for f in files:
                    if f.startswith("backup_") and f.endswith(".sqlite3"):
                        caminho = os.path.join(root, f)
                        try:
                            # Extrair data do nome do arquivo
                            data_str = f.replace("backup_", "").replace(".sqlite3", "")
                            dt_arquivo = datetime.strptime(data_str, "%Y-%m-%d_%H-%M")
                            if dt_arquivo < limite:
                                os.remove(caminho)
                                self.stdout.write(self.style.WARNING(f"Backup antigo removido: {caminho}"))
                        except Exception:
                            # Ignora arquivos fora do padrão
                            pass

        limpar_pasta(pasta_backup_local)
        limpar_pasta(pasta_drive_base)
