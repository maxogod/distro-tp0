# Documentacion ej8

En este ejercicio se mantiene la misma logica confeccionada a lo largo de los ejercicios anteriores, pero permitiendo la posibilidad de manejar las
comunicaciones con los clientes en paralelo.

### Modelo de concurrencia

Para llevar a cabo lo mencionado, se evaluo la posiblidad de implementar multi-threading en el servidor, sin embargo, como el mismo esta codificado
en `python`, tiene el problema de que los threads nunca podran tener paralelismo real, esto se debe al `GIL (global interpreter lock)`. Por esta razon
se decidio utilizar la libreria `multi-processing`, la cual permite trabajar con varias instancias del interprete y evitar el *overhead* de threading.

### Mecanismo de sincronizacion

Los procesos 'workers', una vez que ya recibieron todas las apuestas de su agencia asignada, debera esperar a que todos los workers esten listos, para
luego leer colectivamente (es seguro, siempre y cuando no sea lecto-escritura) el `bet_storage` y enviar a sus clientes la lista de documentos ganadores.

Se utilizan dos mecanismos de sincronizacion a lo largo de este procedimiento:
- Se utiliza un `multiprocessing.Lock` para poder ordenar el acceso de escritura al almacenamiento de apuestas.
- Se utiliza un `multiprocessing.Event` que se utiliza como una **barrera**, ya que el ultimo proceso en terminar de recibir apuestas es el que
dispara el evento y desbloquea a los demas procesos para poder comenzar el sorteo.

### Como ejecutar

La interfaz de uso se dejo sin modificaciones.

```bash
./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construye y ejecuta los servicios
make docker-compose-logs # Verificar salidas
```
