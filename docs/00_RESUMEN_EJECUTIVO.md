# Resumen ejecutivo de la solución

## Origen del proyecto
COTECMAR Conecta IA nace a partir de una oportunidad identificada durante una convocatoria empresarial en Bucaramanga: un alto volumen de proveedores interesados frente a una capacidad limitada del equipo visitante para sostener reuniones individuales y revisar portafolios en tiempo real.

La solución transforma esa dinámica en un proceso digital trazable: captura el interés empresarial desde un QR, estructura la información, conserva los documentos aportados, genera indicadores del evento y permite comparar las capacidades del proveedor contra un catálogo de necesidades activas.

## Objetivo
Facilitar el relacionamiento con proveedores durante giras, cámaras de comercio, ruedas de negocio y convocatorias regionales, reduciendo trabajo manual y acelerando la identificación de empresas con mayor afinidad potencial.

## Flujo funcional
1. COTECMAR crea/activa un evento y publica el QR.
2. El proveedor abre la URL desde el celular.
3. Registra empresa, contacto, ubicación, tamaño, web/LinkedIn y resumen del portafolio.
4. Opcionalmente adjunta PDF o DOCX.
5. La plataforma extrae texto del documento y almacena la información.
6. El motor de análisis clasifica capacidades y calcula afinidad contra necesidades activas.
7. El equipo administrativo consulta indicadores, proveedores, resultados, eventos y necesidades.
8. Los resultados se usan para priorizar revisión humana; no sustituyen procesos formales de habilitación o contratación.

## Estado de la entrega
- MVP funcional desplegado en Railway.
- PostgreSQL administrado conectado.
- Registro público validado.
- Panel administrativo validado.
- Carga y lectura PDF/DOCX implementada.
- Matching con fallback léxico funcional.
- Integración OpenAI preparada; requiere `OPENAI_API_KEY` para análisis semántico real.
- Código fuente y documentación preparados para handover técnico.

## URL del piloto
`https://cotecmar-app-production.up.railway.app`

## Alcance de esta entrega
Esta entrega corresponde a un MVP/piloto funcional. Antes de una operación institucional definitiva se recomienda ejecutar el backlog de hardening, seguridad, gobierno de identidades, trazabilidad, almacenamiento de archivos, respaldo, observabilidad y validación jurídica descrito en `09_BACKLOG_PRODUCCION.md` y `06_SEGURIDAD_DATOS.md`.
