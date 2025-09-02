# Documentacion ej7

En este ejercicio se codifico la logica de sorteo una vez que todas las agencias envian sus apuestas. Para esto se crearon nuevos mensajes
en el protocolo y se agrego una nueva variable de entorno en el servidor. A su vez se hace uso de las funciones de utilidad provistas para
obtener los ganadores sin cargar todas las apuestas en memoria.

### Modificacion de generar-compose.sh

Se agrego al archivo de generacion, una nueva variable de entorno `AGENCIES_AMOUNT` que se inicializa con la cantidad de agencias existentes,
dependiendo con que cantidad de clientes se cree el compose. El uso de la misma en el servidor se explica en dicha seccion.

### Nuevos mensajes de protocolo

Los nuevos tipos de mensajes creados son los siguientes:
- Send/Recieve agency ID
- NotifyBetsFinished
- Send/Receive winner IDs

El primero (envio de agency_id) esta conformado por un header de 1B acompañado de 4B conteniendo el ID de la agencia y
se utiliza para que el servidor lleve la cuenta de que agencias ya terminaron de enviar sus apuestas y cuales no.

El mensaje de notificacion de finalizacion de apuestas es un header de 1B enviado por el cliente para que el servidor no siga esperando mas apuestas del mismo.

El ultimo mensaje es utilizado por el servidor para enviar a la agencia correspondiente, la lista de documentos que ganaron el sorteo. El mismo
esta conformado por un header de 1B, un entero de 4B indicando la cantidad de documentos a enviar, y la lista sin separadores de documentos de 4B.

### Client

El unico cambio en los clientes es la nueva logica de aviso de fin de envio de apuestas, enviado una vez que se llega al `EOF` del archivo de apuestas leido,
y la peticion de documentos ganadores al servidor, para luego escrir un **log** con la cantidad de ganadores.

### Server

Se modifico el `running loop` del servidor para seguir tomando clientes y apuestas hasta que todas las agencias (`AGENCIES_AMOUNT`) hayan terminado de enviar apuestas.
Una vez que se sale de dicho bucle, se lleva a cabo el sorteo, que consta de iterar todas las apuestas guardadas y verificar si su numero es el numero ganador.
Cada vez que se encuentra un ganador, se guarda en la lista de ganadores correspondiente a la agencia de la que vino. Finalmente se envian cada una de dichas listas
a sus respectivas agencias, y posteriormente se finaliza el servidor.

### Como ejecutar

La interfaz de uso se dejo sin modificaciones, exeptuando el mencionado cambio al script de generacion.

```bash
./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construye y ejecuta los servicios
make docker-compose-logs # Verificar salidas
```
