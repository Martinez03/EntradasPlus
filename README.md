
# Proyecto EntradasPlus

Este repositorio contiene la web **EntradasPlus** desarrollada para la asignatura *Aspectos Profesionales de la Informática*. A continuación, se detallan los pasos necesarios para configurar y ejecutar la aplicación en un entorno local.

## Prerrequisitos

- Python 3.x instalado
- `pip` instalado (normalmente incluido con Python)
- Virtualenv (opcional pero recomendado)

## Instrucciones de instalación y ejecución

### 1. Crear un entorno virtual

Es altamente recomendable usar un entorno virtual para evitar conflictos entre dependencias. Sigue los pasos según tu sistema operativo:

#### En Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

Con el entorno virtual activado, instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

Después de instalar las dependencias, inicia el servidor local con el siguiente comando:

```bash
python manage.py runserver
```

### 5. Acceder a la aplicación

Abre tu navegador web y accede a la siguiente URL:

[http://localhost:8000](http://localhost:8000)

