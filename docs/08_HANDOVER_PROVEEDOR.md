# Handover al proveedor de desarrollo

## Estado de entrega
El MVP está funcional y fue validado en Railway con registro público, almacenamiento en PostgreSQL y acceso al panel administrativo.

## Orden recomendado de recepción
1. Clonar repositorio y ejecutar localmente.
2. Revisar `README.md` y documentación de `/docs`.
3. Validar esquema de DB en `app/models.py`.
4. Ejecutar pruebas de registro y login.
5. Conectar el repositorio como fuente oficial del servicio Railway.
6. Recrear secretos en Railway sin copiar valores a Git.
7. Activar `OPENAI_API_KEY` y probar análisis IA.
8. Ejecutar hardening y backlog de producción.

## Criterios mínimos de aceptación técnica
- `/health` = HTTP 200.
- Formulario público sin modal inicial.
- Registro guarda proveedor y documento.
- Botón Finalizar cierra el modal y restablece el formulario.
- Login administrativo funciona.
- Panel inicia sin overlays vacíos.
- QR de evento apunta a URL pública correcta.
- Exportación CSV funciona.
- Con IA habilitada, proveedor finaliza en `analysis_status=done`.

## No incluidos en Git
Credenciales, claves API, contraseña administrativa, secreto de sesión y datos reales de proveedores.
