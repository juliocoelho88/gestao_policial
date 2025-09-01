# Gestão Policial — Sistema de Produtividade e Relatórios

Aplicação **Django** para registrar produções, calcular pontuações por policial (12x36), gerar ranking e exportar relatórios (Excel/CSV).

## Funcionalidades
- Cadastro de Produção (Admin Django com filtros e buscas).
- Cálculo de **pontuação** por evento com pesos configuráveis em `settings.py`.
- **Ranking** por policial.
- **Exportação** de dados para Excel/CSV.
- Organização por **Pelotão** (A, B, C, D etc.).

## Requisitos
- Python 3.11+
- Pip / Virtualenv
- (Opcional) PostgreSQL para produção

## Setup rápido (dev)
```bash
# Clone
git clone https://github.com/SEU-USUARIO/gestao_policial.git
cd gestao_policial

# Ambiente virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt

# Config ..env
copy ..env ..env   # Windows
# cp ..env ..env   # Linux/Mac

# Migrações e usuário admin
python manage.py migrate
python manage.py createsuperuser

# Subir
python manage.py runserver
```

A aplicação, por padrão, usa **SQLite** via `DATABASE_URL` no `.env`. Para produção, configure Postgres.

## Variáveis de ambiente (.env)
Exemplo em `.env.example`:
```bash
DJANGO_SECRET_KEY=changeme
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///./dev.sqlite3
TZ=America/Sao_Paulo
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost
```

## Pesos de Pontuação
Definidos em `settings.py` como `PESOS_PONTUACAO` e lidos pelo model (`Producao.pesos_pontuacao()`).
Para alterar pesos **sem mexer no model**, edite apenas `settings.py`.

```python
# settings.py (trecho)
PESOS_PONTUACAO = {
    "pessoa": 0.01,
    "pessoas_aisp": 0.1,
    "carros": 0.01,
    "carros_aisp": 0.1,
    "motos": 0.01,
    "motos_aisp": 0.1,
    "qnt_ocorrencias": 0.01,
    "flagrantes": 2,
    "flagrantes_aisp": 3,
    "autuacoes": 0.05,
    "raia": 0.05,
    "procurado": 1,
    "carro_apreendido": 0.2,
    "moto_apreendida": 0.2,
    "flagrantes_outros": 0.5,
    "arma": 1,
    "escolas": 0.01,
}
```

## Estrutura (resumo)
```
gestao_policial/
├─ core/                # app principal (models, admin, menu, ranking)
├─ gestao_policial/     # settings, urls, wsgi/asgi
├─ exportados/          # artefatos gerados (ignorado no Git)
├─ manage.py
└─ requirements.txt
```

## CI (GitHub Actions)
Workflow em `.github/workflows/ci.yml` com:
- `flake8`
- `python manage.py check` usando SQLite e uma SECRET_KEY dummy

## Licença
Padrão: **MIT** (arquivo `LICENSE`). Se preferir manter fechado, substitua por *All rights reserved*.
