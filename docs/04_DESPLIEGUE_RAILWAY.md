# Despliegue en Railway

## Topología recomendada
- Servicio web: `cotecmar-app`.
- PostgreSQL administrado: `Postgres`.
- Dominio actual de piloto: `https://cotecmar-app-production.up.railway.app`.

## Variables requeridas
- `DATABASE_URL=${{Postgres.DATABASE_URL}}`
- `ADMIN_PASSWORD` (secreto)
- `SESSION_SECRET` (secreto largo aleatorio)
- `OPENAI_API_KEY` (secreto, opcional para fallback; requerido para IA semántica)
- `OPENAI_MODEL=gpt-5`
- `AI_AUTO_ANALYZE=true`
- `COOKIE_SECURE=true`
- `PUBLIC_BASE_URL=https://<dominio>`
- `MAX_UPLOAD_MB=8`
- `COTECMAR_PRIVACY_URL=<URL política vigente>`

## Flujo recomendado para el proveedor
1. Conectar este repositorio a Railway.
2. Configurar Dockerfile como fuente de build.
3. Crear PostgreSQL y referenciar `DATABASE_URL`.
4. Crear secretos en Railway; nunca en Git.
5. Desplegar y verificar `/health`.
6. Ingresar a `/admin/login`, crear/validar evento y probar un registro real.

## Nota sobre el piloto actual
Durante la construcción se utilizó una carga temporal empaquetada en variables de Railway para superar un bloqueo de acceso del conector GitHub. El proveedor debe migrar el servicio para que el **source of truth sea este repositorio** y eliminar las variables temporales `APP_ARCHIVE_*`, `INDEX_HTML_RAW`, `PUBLIC_JS_RAW` y `DEPLOY_VERSION`.
