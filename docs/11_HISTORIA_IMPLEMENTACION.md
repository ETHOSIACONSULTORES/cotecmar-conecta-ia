# Historia de implementación y decisiones técnicas

## 1. Conceptualización
El producto fue diseñado en tres casos de uso principales:
- captura de proveedores desde QR;
- dashboard de receptividad y caracterización del evento;
- cruce asistido por IA entre capacidades del proveedor y necesidades de COTECMAR.

La experiencia pública se diseñó mobile-first porque el punto de entrada natural es un QR proyectado durante la convocatoria.

## 2. Arquitectura seleccionada
Se optó por una aplicación monolítica liviana en FastAPI para acelerar el MVP y facilitar la transferencia a un proveedor:
- backend y API: FastAPI;
- renderizado: Jinja2;
- frontend: HTML/CSS/JavaScript sin framework;
- persistencia: SQLAlchemy sobre PostgreSQL en producción y SQLite en local;
- documentos: pypdf y python-docx;
- IA: OpenAI Responses API con fallback léxico;
- despliegue: Docker/Railway.

Esta arquitectura reduce dependencias de frontend y permite evolucionar posteriormente a frontend desacoplado si el producto crece.

## 3. Puesta en marcha en Railway
Durante el piloto se creó:
- proyecto Railway privado;
- servicio web;
- PostgreSQL administrado;
- dominio público Railway;
- variables de entorno para base de datos, sesión, administración e IA.

La URL validada del piloto es:
`https://cotecmar-app-production.up.railway.app`

## 4. Incidencias detectadas y correcciones
### Puerto público
El dominio fue configurado inicialmente hacia un puerto distinto al utilizado por Uvicorn. Se normalizó la ejecución utilizando la variable `PORT` de Railway.

### Compatibilidad Starlette/Jinja2
Se presentó un error de `TemplateResponse` por cambio de firma en Starlette. El código fuente final usa argumentos nombrados (`request=`, `name=`, `context=`) y fija `starlette==0.50.0`.

### Modal público visible al cargar
El CSS de overlays usaba `display:grid`, lo que podía competir con el estado `hidden`. La versión final oculta explícitamente el modal público al inicio y lo abre únicamente después de un registro exitoso.

### Modal administrativo vacío
El mismo patrón afectó el overlay de formularios administrativos. La hoja de estilos final incluye reglas globales para respetar `[hidden]` en overlays.

### Caché durante el piloto
Se incorporaron encabezados `no-store` para vistas/activos críticos del piloto y versionado de scripts para evitar que navegadores conservaran recursos anteriores durante iteraciones rápidas.

## 5. Estado del código fuente final
El repositorio entregable ya incorpora las correcciones anteriores de forma nativa. No depende de los parches temporales usados durante las primeras iteraciones de despliegue.

## 6. Consideraciones para el proveedor receptor
El proveedor debe tratar Railway como ambiente piloto y el repositorio Git como fuente oficial. La siguiente evolución debe partir del código versionado, recreando secretos de forma segura y evitando trasladar credenciales del piloto al repositorio.
