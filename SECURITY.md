# Security Policy — MVP

Este repositorio contiene un MVP y no debe considerarse endurecido para operación institucional sin ejecutar el backlog de seguridad.

## Secretos
Nunca registrar en Git:
- `OPENAI_API_KEY`
- `ADMIN_PASSWORD`
- `SESSION_SECRET`
- credenciales PostgreSQL
- tokens de GitHub/Railway
- datos personales reales de proveedores

Use variables de entorno y gestores de secretos del proveedor de nube.

## Reporte de hallazgos
Los hallazgos de seguridad deben gestionarse de forma privada con el responsable técnico del proyecto. No publicar credenciales, datos personales, exploits ni evidencia sensible en issues públicos.

## Controles pendientes para producción
Consulte `docs/06_SEGURIDAD_DATOS.md` y `docs/09_BACKLOG_PRODUCCION.md`.
