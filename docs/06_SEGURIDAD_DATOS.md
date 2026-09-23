# Seguridad y protección de datos

## Implementado en el MVP
- Consentimiento obligatorio antes de registrar.
- Enlace a política de tratamiento de datos.
- Sesión administrativa HTTP-only y SameSite Strict.
- `COOKIE_SECURE=true` en producción.
- Credenciales y API keys mediante variables de entorno.
- Documentos accesibles solo por endpoints administrativos autenticados.
- Límite de tamaño y formatos PDF/DOCX.

## Requerido antes de operación institucional
- SSO/MFA y perfiles por rol.
- Bitácora/auditoría de accesos y cambios.
- Antivirus/antimalware de adjuntos.
- Cifrado y política de retención/expurgo.
- Backups probados y recuperación.
- WAF/rate limiting/CSRF según arquitectura final.
- Gestión de vulnerabilidades y pruebas de penetración.
- Revisión jurídica del consentimiento y evaluación de transferencia/tratamiento con servicios de IA.
- Migrar binarios a almacenamiento de objetos para escala.

## Secretos
Nunca versionar `OPENAI_API_KEY`, `ADMIN_PASSWORD`, `SESSION_SECRET` ni credenciales de base de datos.
