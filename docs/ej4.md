# Documentacion ej4

En este ejercicio se agregaron al cofigo fuente del servidor y de los clientes, manejadores de `signals` (especificamente para `SIGTERM`),
para cerrar el programa de forma ordenada y sin dejar recursos sin liberar.

### Server

Se creo una funcion 'helper' y se vincula a dicha *signal* utilizando el modulo de python [signal], cuando esta es invocada,
ejecuta el cierre (shutdown) del servidor. Para esto el servidor cierra
las comunicaciones y cambia la condicion de *running* a False.

### Client

En el caso de los clientes se creo una `GoRoutine` que espera de forma bloqueante la ocurrencia de la *signal* y
posteriormente envia un mensaje a travez de un canal usado especificamente para comunicar *shutdowns* a las demas
*GoRoutines*. El *client loop* utiliza un bloque `select` para evaluar si se recibio un mensaje a travez de dicho canal
y cerrar ordenadamente el programa, sino, se continua con el resto de la logica de negocio, y al terminar la iteracion
vuelve a ejecutar los mismos pasos hasta que se produzca un *shutdown* o se termine la logica.
