# Instalación local

## Opción A: Python + SQLite
1. Instalar Python 3.12.
2. `python -m venv .venv`
3. Activar el entorno.
4. `pip install -r requirements.txt`
5. Copiar `.env.example` a `.env` y cargar las variables en el entorno.
6. Ejecutar `uvicorn app.main:app --reload --port 8000`.
7. Abrir `http://localhost:8000`.

## Opción B: Docker Compose + PostgreSQL
`docker compose up --build`

El panel se encuentra en `/admin/login`. No utilice las credenciales de ejemplo en entornos compartidos.
