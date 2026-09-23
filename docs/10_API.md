# API principal

## Público
- `GET /health` — estado del servicio.
- `GET /api/public/event?code=` — evento activo.
- `POST /api/providers` — alta de proveedor y documento.

## Autenticación
- `POST /api/admin/login` — crea sesión.
- `POST /api/admin/logout` — cierra sesión.

## Administración
- `GET /api/admin/summary` — dashboard/base.
- `GET /api/admin/providers/{id}` — ficha.
- `GET /api/admin/providers/{id}/document` — descarga documento.
- `POST /api/admin/providers/{id}/reanalyze` — reanálisis.
- `POST /api/admin/events` — crea evento.
- `GET /api/admin/events/{id}/qr` — QR.
- `POST /api/admin/needs` — crea necesidad.
- `GET /api/admin/export.csv` — exportación.

Consultar `app/main.py` como contrato técnico definitivo del MVP.
