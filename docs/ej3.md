# Documentacion ej3

En esta seccion se escribio un segundo script de `bash` cuyo proposito es verificar el correcto funcionamiento del servidor **echo**.
Para esto se crea y corre un container temporal a partir de la imagen (liviana) `busybox:latest` y se le asigna la red interna definida en el docker-compose.yaml y mencionada en el **ej1**,
luego se utiliza `netcat` para comunicarse con el servidor, enviar un mensaje, esperar la respuesta y corroborar que cumpla la funcionalidad "echo"
(es decir que el mensaje de salida sea igual al de entrada), finalmente el container se auto-elimina.

### Como ejecutar

```bash
make docker-compose-up # Construir y correr el compose
# Server corriendo
./validar-echo-server.sh # Imprime mensajes de 'success' o 'fail'
```
