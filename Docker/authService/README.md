# Trabajo teoricopráctico 1 - API REST

## Miembros del equipo
Trabajo realizado por:
- Álvaro Fernandez Santos
- Daniel Almansa Rodríguez

## Requisitos
Existe un archivo _requirements.txt_ para facilitar la instalación:
```shell
pip install -r requeriments.txt
```

## Ejecución
Para el servidor, instalar el paquete y ejecutar:
```shell
authService_server -a <admin_token> -p <port> -l <ip_listening> -d <database_path>
```

## Tests
Se puede ejectuar la batería de tests desde la carpeta raíz:
```shell
pip install tox
tox
```
