# Trabajo teoricopráctico 2 - API REST

## Miembros del equipo
Trabajo realizado por:
- Álvaro Fernandez Santos
- Daniel Almansa Rodríguez


## Ejecución
Se dispone de un Makefile para facilitar la ejecución del servidor y sus pruebas:
Para ejecutar el servidor:
```shell
make all
```
Por defecto escuchará en la IP 172.17.0.2:3001

Para facilitar su uso se puede añadir con el sobrenombre auth.local utilizando:
```shell
make add_server
```
Y se puede eliminar de la misma forma:
```shell
make remove_server
```

## Tests
Se pueden ejectuar de la siguiente forma:
```shell
make tests
```
