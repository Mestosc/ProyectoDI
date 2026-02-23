.. Proyecto GTK DI documentation master file, created by
   sphinx-quickstart on Mon Feb  9 09:40:52 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Proyecto GTK DI: Rastreador de Lectura de Libros
===============================================

Bienvenido a la documentación de **Proyecto GTK DI**, una aplicación de escritorio intuitiva diseñada para gestionar tu biblioteca personal y realizar un seguimiento detallado de tu progreso de lectura.

Descripción del Proyecto
------------------------
Este sistema permite a los usuarios organizar sus libros por géneros y registrar el avance diario de sus lecturas. La aplicación está construida utilizando **Python** y **GTK** (PyGObject), ofreciendo una interfaz gráfica moderna y funcional para sistemas Linux.

Características Principales
--------------------------
*   **Gestión Integral:** Añade, edita y organiza tus libros fácilmente.
*   **Control de Progreso:** Registra el número de páginas leídas para visualizar tu avance en cada obra.
*   **Base de Datos Local:** Utiliza SQLite para almacenar toda la información de forma segura y eficiente en el archivo ``libros.db``.
*   **Interfaz GTK:** Una experiencia de usuario nativa y fluida.

Requisitos e Instalación
------------------------

Para ejecutar este proyecto, necesitarás tener instalado **Python 3** y las librerías de desarrollo de **GTK** (como ``libgirepository1.0-dev`` en Ubuntu/Debian).

Sigue estos pasos para la instalación:

1.  **Clonar el repositorio** y acceder a la carpeta del proyecto.
2.  **Crear un entorno virtual** (opcional):

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate

3.  **Instalar dependencias**:

   .. code-block:: bash

      pip install -r requirements.txt

Uso de la Aplicación
--------------------

Para iniciar el rastreador de lectura, simplemente ejecuta el script principal desde la raíz del proyecto:

.. code-block:: bash

   python src/main.py

Tabla de Contenidos
-------------------

.. toctree::
   :maxdepth: 2
   :caption: Guías y Módulos:

   funcionamiento_usuario
   modules

Indices y tablas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
