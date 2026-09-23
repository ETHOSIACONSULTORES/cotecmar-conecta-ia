# Arquitectura técnica

```text
Proveedor móvil / navegador
        | HTTPS
        v
FastAPI + Jinja2 + JS/CSS
        |---------------------> OpenAI Responses API (opcional)
        |
        v
PostgreSQL
  - eventos
  - necesidades
  - proveedores
  - documentos
  - resultados IA
```

## Componentes
- **FastAPI**: API y renderizado web.
- **Jinja2**: plantillas del registro, login y panel.
- **PostgreSQL/SQLAlchemy**: persistencia.
- **pypdf/python-docx**: extracción documental.
- **OpenAI Responses API**: clasificación y matching semántico estructurado.
- **qrcode**: generación de QR por evento.

## Decisiones relevantes
- La clave de IA solo existe en backend.
- El documento se almacena en DB en el MVP; para alto volumen se recomienda object storage.
- El scoring sirve para priorización humana, no contratación automática.
- Existe fallback léxico si no se configura IA.
