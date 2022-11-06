# Trabajo teoricopráctico 1 - API REST

Demostración para **Python 3** de API REST creando un servidor de autenticación con Flask y un cliente con requests.

Crear un entorno virtual y activarlo:
```shell
python3 -m venv .venv
source .venv/bin/activate
```

Instalar las dependencias:
```shell
pip install -r requeriments.txt
```

Se puede lanzar en un terminal el servidor:
```shell
python3 authService_scripts/server.py
```

Podemos lanzar la *test suite* utilizando *Tox*:
```shell
pip install tox
tox
```
