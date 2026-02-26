# Learn Flask using uv and Gunicorn

## Inspired by Devscale Bootcamp AI Enabled Python Web Development

## 🚀 Flask Bootcamp API (Feature-based Modular Architecture)

Proyek ini adalah API backend yang dibangun dengan **Flask**, **SQLAlchemy**, dan **Pydantic** menggunakan pendekatan **Vertical Slice Structure (Feature-based Modular Architecture)**. Manajemen package dilakukan menggunakan **uv** untuk performa maksimal.

### 🏗️ Project Structure

```text
app/
├── modules/          # Kontainer Fitur (Vertical Slices)
│   ├── trainer/      # Modul Trainer (Entity, Repo, Service, Router)
│   └── bootcamp/     # Modul Bootcamp (Entity, Repo, Service, Router)
├── core/             # Konfigurasi Global (Database, Settings)
├── main.py           # Entry Point & Konfigurasi OpenAPI
└── __init__.py
```

🛠️ Tech Stack

    Framework: Flask

    Package Manager: uv

    Documentation: Scalar

    Database: SQLite (SQLAlchemy ORM)

    Validation: Pydantic v2

    Migrations: Alembic

🚀 Memulai Cepat (Quick Start)

1. Prasyarat

Pastikan Anda sudah menginstall uv di mesin Anda:

```Bash
curl -LsSf https://astral.sh/uv/install.sh | sh

atau

pip install uv
```

2. Instalasi Dependency

Gunakan uv untuk menyinkronkan environment:

```Bash
uv sync --extra scalar
```

3. Menjalankan Aplikasi

Jalankan server pengembangan menggunakan Gunicorn atau Flask CLI:

```Bash
uv run gunicorn -w 1 'app.main:app'
```

Aplikasi akan berjalan di: http://127.0.0.1:8000

📖 Dokumentasi API (Scalar)

Proyek ini menggunakan Scalar untuk dokumentasi interaktif yang modern. Anda dapat mengaksesnya di:

    Scalar UI: http://127.0.0.1:8000/openapi/scalar

    Swagger UI: http://127.0.0.1:8000/openapi/swagger

    Redocly UI: http://127.0.0.1:8000/openapi/redoc

    OpenAPI JSON: http://127.0.0.1:8000/openapi/openapi.json

🧪 Testing API

Untuk melakukan testing, Anda bisa menggunakan UI Scalar di atas atau menggunakan curl:

```Bash
curl -X GET http://127.0.0.1:8000/trainers/
```

🗃️ Database Migrations

Gunakan Alembic untuk memperbarui skema database:
Bash

# Inisialisasi migrasi baru

```
uv run alembic revision --autogenerate -m "Initial migration"
```

# Update database

```
uv run alembic upgrade head
```

Dibuat dengan ❤️ menggunakan Python & Flask.
