# Sugerido python 3.12 o superior
# proyecto-hci
Para el proyecto se requiere un entorno virtual, puedes crear uno ejecutando:
```sh
python -m venv venv
```
Y lo activas:
```sh
source venv/Scripts/activate # windows
./venv/bin/activate # unix
```
Primero instala las dependencias desde el archivo `requirements.txt`.
```sh
pip install -r requirements.txt
```
Una vez que ya hayas instalado otras dependencias, ejecuta el siguiente
comando para actualizar las dependencias con las que ya poseías previamente.
```sh
pip freeze > requirements.txt
```

