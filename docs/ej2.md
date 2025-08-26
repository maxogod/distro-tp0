# Documentacion ej2

Se modifico el previamente confeccionado script `generar-compose.sh` de manera que los archivos de configuracion
del servidor ("config.ini") y de los clientes ("config.yaml") se monten a los containers cuando los mismos se ejecutan,
en lugar de ser copiados a la imagen estatica de dichos servicios.

Esto permite la posterior modificacion de los archivos y que esto se refleje en los contenedores (dinamicamente).

### Como ejecutar

La interfaz de uso se dejo sin modificaciones.

```bash
./generar-compose.sh <archivo_salida> <cantidad_clientes>
# e.g. ./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construir y correr el compose
```
