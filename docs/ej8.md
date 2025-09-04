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
- Se utiliza un `multiprocessing.Barrier` para lograr que todos los procesos una vez terminan de recibir
apuestas por parte de su agencia, esperen a que el resto termine. Una vez que todos terminan de recibir, se desbloquean y
se lleva a cabo el sorteo, es decir, pasan a obtener los dnis ganadores de su agencia y enviarlos.

### Como ejecutar

La interfaz de uso se dejo sin modificaciones.

```bash
./generar-compose.sh docker-compose-dev.yaml 5
make docker-compose-up # Construye y ejecuta los servicios
make docker-compose-logs # Verificar salidas
```
