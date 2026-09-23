# Operación del panel administrativo

## Acceso
`/admin/login` solicita una clave definida mediante `ADMIN_PASSWORD`. La sesión se guarda en cookie HTTP-only por 12 horas.

## Dashboard
Muestra volumen total, proveedores analizados/pendientes, afinidad promedio, alta afinidad, ciudades y sectores.

## Proveedores
Permite consultar ficha, contacto, ciudad, tamaño, sector, score, estado del análisis, documento original y detalle del matching.

## Eventos y QR
Crear un evento genera un `public_code` único. El QR debe dirigir a `/?event=<public_code>`.

## Necesidades
El catálogo activo alimenta el análisis. Antes de cada gira se recomienda depurar necesidades vigentes y desactivar las obsoletas.

## Exportación
`/api/admin/export.csv` exporta la base consolidada para análisis adicional.
