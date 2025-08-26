# Documentacion ej1

En este ejercicio se escribio un simple script de `bash` que formatea y escribe un archivo `yaml`
representando una configuracion de docker-compose, conteniendo un servidor que utiliza la imagen `server:latest` y
una cantidad dinamica de clientes que utilizan la imagen `client:latest`. Todos los servicios mencionados se comunican
entre si utilizando la red interna configurada `testing_net`.

### Como ejecutar

```bash
./generar-compose.sh <archivo_salida> <cantidad_clientes>
# e.g. ./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construir y correr el compose
```
