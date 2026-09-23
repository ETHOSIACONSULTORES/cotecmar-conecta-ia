# Checklist de recepción técnica

## Repositorio
- [ ] Clonar `ETHOSIACONSULTORES/cotecmar-conecta-ia`.
- [ ] Revisar `README.md`, `CHANGELOG.md` y `/docs`.
- [ ] Confirmar que no existan secretos reales versionados.
- [ ] Crear rama de trabajo y política de revisión de cambios.

## Ejecución local
- [ ] Crear entorno Python 3.12.
- [ ] Instalar `requirements.txt`.
- [ ] Copiar `.env.example` a un archivo local de variables.
- [ ] Definir `ADMIN_PASSWORD` y `SESSION_SECRET` seguros.
- [ ] Levantar aplicación y validar `/health`.
- [ ] Validar formulario público.
- [ ] Validar login y dashboard.

## Base de datos
- [ ] Probar SQLite para desarrollo.
- [ ] Probar PostgreSQL para integración.
- [ ] Revisar modelos y estrategia de migraciones.
- [ ] Implementar Alembic antes de evolución productiva.

## Documentos
- [ ] Probar PDF con texto seleccionable.
- [ ] Probar DOCX.
- [ ] Validar límite de tamaño.
- [ ] Definir antivirus, OCR y object storage para producción.

## IA
- [ ] Configurar `OPENAI_API_KEY` únicamente en secrets del ambiente.
- [ ] Confirmar `analysis_status=done`.
- [ ] Revisar prompts, estructura de salida y scoring.
- [ ] Validar resultados con usuarios de Compras antes de uso institucional.

## Railway
- [ ] Conectar el repositorio Git como fuente oficial del servicio.
- [ ] Mantener PostgreSQL como servicio separado.
- [ ] Configurar dominio/HTTPS.
- [ ] Configurar variables descritas en `.env.example`.
- [ ] Probar redeploy desde Git.
- [ ] Configurar backups y observabilidad.

## Seguridad
- [ ] Rotar todas las credenciales del piloto al recibir el proyecto.
- [ ] Implementar SSO/MFA y roles.
- [ ] Auditoría de accesos y acciones.
- [ ] Rate limiting/CSRF/WAF según arquitectura final.
- [ ] Prueba de vulnerabilidades y penetración.
- [ ] Revisión jurídica de consentimiento y tratamiento con IA.

## Criterios de aceptación
- [ ] `/health` retorna HTTP 200.
- [ ] El formulario carga sin overlays iniciales.
- [ ] Un proveedor puede registrarse y adjuntar documento.
- [ ] `Finalizar` restablece el formulario.
- [ ] El panel administrativo carga sin overlays vacíos.
- [ ] La ficha del proveedor muestra información y análisis.
- [ ] Eventos y necesidades son administrables.
- [ ] Exportación CSV funciona.
