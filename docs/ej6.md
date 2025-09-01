# Documentacion ej6

En este ejercicio se agrega una nueva funcionalidad al sistema, que consiste en el envio, recepcion y manejo de batches de apuestas, de manera de
minimizar la cantidad de mensajes que se envian por agencia. Para esto se hicieron modificaciones a la logica existente y se crearon nuevos mensajes de protocolo.

### Modificacion de generar-compose.sh

Se modifico el script de manera de agregar un nuevo volumen para los Clients. Dependiendo el id de cliente correspondiente
se le monta el volumen `agency-{clientID}.csv` y se mapea al path `/agency.csv` dentro del container.

### Modificacion de protocolo y batch-size

El metodo `enviar/recibir apuesta` fue reemplazado por su version mas general `enviar/recibir batch de apuestas`.

El mensaje enviado por dicho metodo es similar al anteriormente utilizado pero ahora se utiliza un header mas que contiene la cantidad de apuestas presentes
en el batch.

```raw
[1-Byte data header][4-Byte batch-size in BigEndian]  [4-Byte length in BigEndian][Bet as string]  [4-Byte][Bet-2]  ...

e.g. 0x01 0x0000000A 0x00000026nombre|apellido|30111222|2000-01-30|14 ... las 9 apuestas restantes
```

La confirmacion por parte del servidor para avisar que recibio correctamente el batch, se mantuvo intacto.

A su vez en la configuracion del cliente `config.yaml` se actualizo el valor de `batch.maxAmount` a **120** para mantener los paquetes por debajo de 8KB.
Esto se calculo tomando la linea mas larga de los archivos de agencias (~56B) y teniendo en cuenta que cada apuesta tendra 4B adicionales con su largo,
y que ademas hay 5B extra por el header. De esta forma si hay 120 apuestas de 56B el paquete medira aproximadamente 7.03KB, dejando un margen de 1KB en caso
de que haya registros incluso mas largos.

### Client

Se creo una funcion `betBatchGenerator` que lee el archivo "agency-{n}.csv" correspondiente y empaqueta cada registro en una lista de apuestas,
de largo `batch.maxAmount (config)`. Esta funcion corre en una Go-routine tomando el rol de productor sobre un canal de batches, y la Go-routine principal
toma el rol de consumidor de dicho canal, hasta que el mismo se cierra cuando ya se termino de leer el archivo.

Para cada batch se utiliza el protocolo para enviarlo al servidor y luego esperar por la confirmacion de recepcion.

<small>Observacion: cuando hay una entrada malformada se ignora y no se agrega al batch</small>

### Server

En el caso del servidor no se hicieron modificaciones significativas. Este en lugar de utilizar el antiguo metodo `receive_bet` ahora utiliza
`receive_bet_batch`, guarda esa informacion con la funcion de utilidad `store_bets` y luego envia al cliente la confirmacion de recepcion.

### Como ejecutar

La interfaz de uso se dejo sin modificaciones, exeptuando el mencionado cambio al script de generacion.

```bash
./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construye y ejecuta los servicios
make docker-compose-logs # Verificar salidas
```
