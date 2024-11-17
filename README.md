# Proyecto EntradasPlus

Este repositorio contiene la web EntradasPlus para la asignatura Aspectos Profesionales de la Informatica. A continuación, se detallan los pasos necesarios para configurar y ejecutar la aplicación en un entorno local.

## Prerrequisitos

- Python 3.x instalado en tu máquina
- `pip` instalado (normalmente incluido con Python)
- Virtualenv (opcional pero recomendado)

---

## Instrucciones de instalación y ejecución

### 1. Crear un entorno virtual

Es altamente recomendable usar un entorno virtual para evitar conflictos entre dependencias. Para crear y activar un entorno virtual, sigue estos pasos:

#### En Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate

En Windows:
bash
Copiar código
python -m venv venv
venv\Scripts\activate
2. Instalar dependencias
Con el entorno virtual activado, instala las dependencias necesarias usando el archivo requirements.txt:

bash
Copiar código
pip install -r requirements.txt
3. Realizar migraciones de la base de datos
Aplica las migraciones necesarias para configurar las tablas en la base de datos local:

bash
Copiar código
python manage.py migrate
4. Ejecutar el servidor de desarrollo
Inicia el servidor de desarrollo de Django:

bash
Copiar código
python manage.py runserver
5. Acceder a la aplicación
Una vez que el servidor esté en funcionamiento, abre tu navegador web y accede a la siguiente URL:

arduino
Copiar código
http://localhost:8000
Si todo está configurado correctamente, deberías ver la página principal de la aplicación EntradasPlus.
