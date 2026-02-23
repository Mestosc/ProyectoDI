# Proyecto GTK DI - Rastreador de Lectura de Libros

Este proyecto es una aplicación de escritorio desarrollada con **Python** y **GTK** (PyGObject) diseñada para gestionar una biblioteca personal de libros, permitiendo realizar un seguimiento detallado del progreso de lectura.

## Características Principales

*   **Gestión de Libros:** Permite añadir, editar y organizar libros en una base de datos local.
*   **Seguimiento de Progreso:** Registra las páginas que has leído de cada libro para mantener un control de tu avance.
*   **Base de Datos SQLite:** Almacena toda la información de forma persistente y eficiente en un archivo local (`libros.db`).
*   **Documentación Integrada:** Incluye documentación técnica generada automáticamente con **Sphinx**.

## Estructura del Proyecto

*   `src/`: Contiene el código fuente de la aplicación.
    *   `main.py`: Punto de entrada de la aplicación.
    *   `controller.py`: Lógica de negocio y gestión de la base de datos SQLite.
    *   `ventana_principal.py`: Interfaz gráfica principal del usuario.
    *   `formulario_anadir_datos.py`: Ventana para la entrada de nuevos libros.
    *   `libro.py`: Modelos de datos para Libros y Autores.
*   `source/`: Archivos de configuración y fuentes para la documentación de Sphinx.
*   `libros.db`: Archivo de la base de datos SQLite.
*   `requirements.txt`: Lista de dependencias del proyecto.

## Requisitos Previos

Asegúrate de tener instalado Python 3 y las librerías de desarrollo de GTK en tu sistema (ej. `libgirepository1.0-dev` en sistemas basados en Debian/Ubuntu).

## Instalación

1.  Clona este repositorio o descarga los archivos.
2.  Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # o
    venv\Scripts\activate  # En Windows
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
python src/main.py
```

## Documentación

Para generar la documentación en formato HTML, puedes usar el comando:

```bash
sphinx-build -b html source build/html
```

---
**Autor:** Oscar Rodriguez - 2026
