# creacion de entorno
```sh
py -m venv env
```
# dar permisos siempre que inicie dar permisos
```sh
cd env
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
# activar entorno
```sh
cd Scripts
./activate
```
# desactivar
```sh
deactivate
```
# saber las lib
```sh
pip freeze
```
# auto lib del entorno
```sh
pip freeze > requirements.txt 
```
# instalar la lib auto
```sh
pip install -r requirements.txt
```
# iniciar servidor uvicorn
```sh
uvicorn main:app --reload
```
# elegir puerto y en red 
```sh
uvicorn main:app --reload --port 5000 --host 0.0.0.0
```
