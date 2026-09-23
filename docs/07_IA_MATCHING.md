# Motor de IA y matching

## Entrada
- Datos declarados por el proveedor.
- Resumen escrito.
- Texto extraído de PDF/DOCX.
- Catálogo de necesidades activas.

## Salida estructurada
- Sector.
- Resumen ejecutivo.
- Categorías, productos, servicios y capacidades.
- Certificaciones identificadas con evidencia.
- Fortalezas y brechas.
- `overall_score` 0–100.
- Clasificación de afinidad.
- Hasta cinco necesidades relacionadas con score, racional y evidencia.
- Próximo paso recomendado.

## Principios
- No inventar experiencia, clientes ni certificaciones.
- Penalizar ausencia de evidencia.
- Explicar por qué existe una coincidencia.
- El resultado prioriza revisión humana; no decide contratación.

## Fallback
Sin `OPENAI_API_KEY` se ejecuta un matching léxico conservador para mantener el flujo operativo, identificado explícitamente como análisis de contingencia.
