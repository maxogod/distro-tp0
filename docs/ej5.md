# Documentacion ej5

En este ejercicio se llevo a cabo un cambio de logica de negocio de `echo server` a `agencia de quiniela`. Donde
los clientes envian apuestas y el server se encarga de confirmarlas y guardarlas en su base de datos y haciendo *logs* informativos
a lo largo del proceso.

### Nuevas variables de entorno

Dado que el test de el presente ejercicio no inyecta variables de entorno con la informacion del cliente, se
agregaron las mismas al script de generacion de `docker-compose.yaml`.

Las mismas son:

- CLI_NOMBRE
- CLI_APELLIDO
- CLI_DOCUMENTO
- CLI_NACIMIENTO
- CLI_NUMERO

### Protocolo

El protocolo creado es simple ya que la logica lo amerita, y cuenta con las 2 siguientes operaciones:

- Enviar/Recibir apuesta
- Enviar/Recibir confirmacion

El formato del mensaje `apuesta` es un header conteniendo el largo de la misma seguido por una cadena de caracteres.
La representacion de la apuesta como cadena lleva el formato `campo1|campo2|...` (luego se crea un objeto Bet del dominio a partir de la cadena).

```raw
[4-Byte length header BigEndian][Bet as string]

e.g. 0x00000026nombre|apellido|30111222|2000-01-30|14
```

El mensaje de `confirmacion` es un simple byte, utilizado como header y con el valor `0x01`.

```
[1-Byte confirmation header]

e.g. 0x01
```

### Nueva estructura

Se altero un poco la estructura del repositorio para separar la logica de comunicacion de la logica de negocio mas eficazmente.

Dentro de ambos directorios `client` y `server` se crearon modulos `bets` con submodulos `models` (donde se guardan los objetos del dominio)
y `protocol` (donde se encapsula la logica del protocolo y comunicaciones).

En el caso del server tambien se movio el archivo `utils.py` al modulo `bets` ya que contiene funciones sobre el dominio.

**Overview de la estructura**:
```bash
.
├── client
│   ├── bets # new module
│   │   ├── models # new sub-module
│   │   └── protocol # new sub-module
│   ├── common
│   │   └── client.go
│   ├── config.yaml
│   ├── Dockerfile
│   └── main.go
│
├── server
│   ├── bets # new module
│   │   ├── __init__.py
│   │   ├── models # new sub-module
│   │   ├── protocol # new sub-module
│   │   └── utils.py
│   ├── common
│   │   ├── __init__.py
│   │   └── server.py
│   ├── config.ini
│   ├── Dockerfile
│   ├── main.py
│   └── tests
│       └── test_common.py
```

### Como ejecutar

La interfaz de uso se dejo sin modificaciones, exeptuando el mencionado cambio al script de generacion.

```bash
./generar-compose.sh docker-compose-dev.yaml 5 # Contiene las nuevas variables de entorno
make docker-compose-up # Construye y ejecuta los servicios
make docker-compose-logs # Verificar salidas
```
