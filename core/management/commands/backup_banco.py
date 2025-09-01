import os
import shutil
from django.core.management.base import BaseCommand
from datetime import datetime
from django.conf import settings

class Command(BaseCommand):
    help = 'Cria um backup do banco de dados SQLite com data no nome'

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_backup = f"backup_{data}.sqlite3"
        pasta_backup = os.path.join(settings.BASE_DIR, 'backups')

        os.makedirs(pasta_backup, exist_ok=True)

        destino = os.path.join(pasta_backup, nome_backup)
        shutil.copy2(db_path, destino)

        self.stdout.write(self.style.SUCCESS(f"Backup criado em: {destino}"))
