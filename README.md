# COTECMAR Conecta IA

Plataforma web **mobile-first** para digitalizar el relacionamiento con proveedores durante convocatorias regionales: captura desde QR, lectura de portafolios PDF/DOCX, dashboard de receptividad y matching asistido por inteligencia artificial contra necesidades activas de COTECMAR.

> **Estado:** MVP funcional desplegado y validado en Railway. La IA semántica requiere `OPENAI_API_KEY`; sin ella existe un fallback léxico.

## Problema que resuelve
En convocatorias con alta asistencia, el equipo de COTECMAR no puede sostener entrevistas individuales con todos los empresarios. Conecta IA transforma ese momento en un flujo digital estructurado: cada participante registra capacidades desde su celular y el equipo obtiene una base consolidada, indicadores y priorización explicable.

## Módulos
- **Registro de proveedores por QR** con datos, ciudad, tamaño, web/LinkedIn, resumen, PDF/DOCX y consentimiento.
- **Extracción documental** de PDF con texto seleccionable y DOCX.
- **Dashboard administrativo** con volumen, ciudades, sectores, afinidad y estado de análisis.
- **Eventos y QR** para giras/convocatorias.
- **Catálogo de necesidades** administrable.
- **Matching IA explicable** 0–100, fortalezas, brechas, evidencia y próximo paso.
- **Exportación CSV** y descarga autenticada de documentos.

## Stack
Python 3.12 · FastAPI · Starlette 0.50 · SQLAlchemy · PostgreSQL/SQLite · Jinja2 · Vanilla JS/CSS · OpenAI Responses API · pypdf · python-docx · qrcode.

## Inicio rápido
```bash
python -m venv .venv
# activar entorno
pip install -r requirements.txt
# configurar variables según .env.example
uvicorn app.main:app --reload --port 8000
```

Abrir:
- Registro público: `http://localhost:8000/`
- Panel: `http://localhost:8000/admin/login`
- Healthcheck: `http://localhost:8000/health`

También puede ejecutarse con `docker compose up --build`.

## Variables de entorno
| Variable | Requerida | Propósito |
|---|---|---|
| `DATABASE_URL` | Sí en producción | PostgreSQL/SQLite |
| `ADMIN_PASSWORD` | Sí | Acceso administrativo |
| `SESSION_SECRET` | Sí | Firma de sesión |
| `OPENAI_API_KEY` | Para IA semántica | Análisis y matching |
| `OPENAI_MODEL` | No | Modelo, default `gpt-5` |
| `AI_AUTO_ANALYZE` | No | Análisis automático |
| `COOKIE_SECURE` | Sí en HTTPS | Cookie segura |
| `PUBLIC_BASE_URL` | Recomendado | QR y URL pública |
| `MAX_UPLOAD_MB` | No | Límite de adjunto |
| `COTECMAR_PRIVACY_URL` | Sí | Política de datos |

**No versionar valores secretos.**

## Despliegue Railway
El repositorio incluye `Dockerfile` y `railway.toml`. Crear un PostgreSQL en el mismo proyecto y configurar `DATABASE_URL=${{Postgres.DATABASE_URL}}`. Consulte `docs/04_DESPLIEGUE_RAILWAY.md`.

Piloto actual: `https://cotecmar-app-production.up.railway.app`

## Estructura
```text
app/
  main.py             API y rutas
  ai.py               análisis IA/fallback
  auth.py             sesión administrativa
  db.py               conexión SQLAlchemy
  document.py         lectura PDF/DOCX
  models.py           modelo de datos
  seed.py             datos iniciales
  templates/          frontend Jinja2
  static/             CSS, JS, logo
docs/                 documentación de entrega
Dockerfile
docker-compose.yml
railway.toml
render.yaml
.env.example
```

## Documentación de entrega
0. [Resumen ejecutivo](docs/00_RESUMEN_EJECUTIVO.md)
1. [Alcance funcional](docs/01_ALCANCE_FUNCIONAL.md)
2. [Arquitectura](docs/02_ARQUITECTURA.md)
3. [Instalación local](docs/03_INSTALACION_LOCAL.md)
4. [Despliegue Railway](docs/04_DESPLIEGUE_RAILWAY.md)
5. [Operación administrativa](docs/05_OPERACION_ADMIN.md)
6. [Seguridad y datos](docs/06_SEGURIDAD_DATOS.md)
7. [IA y matching](docs/07_IA_MATCHING.md)
8. [Handover al proveedor](docs/08_HANDOVER_PROVEEDOR.md)
9. [Backlog de producción](docs/09_BACKLOG_PRODUCCION.md)
10. [API principal](docs/10_API.md)
11. [Historia de implementación](docs/11_HISTORIA_IMPLEMENTACION.md)
12. [Checklist de recepción](docs/12_CHECKLIST_ENTREGA.md)

Adicionalmente: [Política de seguridad del MVP](SECURITY.md).

## Criterios de uso
El score de IA es una **herramienta de priorización para revisión humana**. No debe utilizarse como decisión automática de contratación, habilitación o adjudicación.

## Próxima fase recomendada
SSO/MFA, roles, auditoría, object storage, antivirus/OCR, backups, Alembic, observabilidad, pruebas de seguridad, validación formal del scoring e integración con sistemas corporativos.


## Propiedad y transferencia técnica
La entrega técnica se realiza mediante el repositorio privado `ETHOSIACONSULTORES/cotecmar-conecta-ia`. El proveedor receptor debe trabajar desde Git como fuente oficial y recrear todas las credenciales mediante secretos del ambiente. El repositorio no contiene contraseñas ni API keys reales.
