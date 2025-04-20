# Proyecto de Microondas Inteligente con Flask y Docker

Este proyecto simula la funcionalidad de un microondas inteligente a través de una interfaz web construida con Flask (Python). Permite a los usuarios ver una lista de recetas, personalizar el tiempo de cocción y simular el proceso de "enviar al horno".

## Funcionalidades Principales:

* **Lista de Recetas:** Muestra una lista de recetas cargadas desde un archivo `recetas.json`.
* **Enviar al Horno:** Simula el envío de una receta al "horno" y muestra un mensaje de inicio y finalización de la cocción con un tiempo simulado.
* **Personalizar Receta:** Permite modificar el tiempo de cocción de una receta antes de "enviarla al horno".

## Despliegue Local

A continuación, se describen dos métodos para desplegar la aplicación localmente: utilizando Docker y utilizando un entorno virtual (venv).

### Opción 1: Despliegue con Docker (Recomendado)

Este método asegura un entorno consistente y aislado para ejecutar la aplicación.

**Prerequisites:**

* [Docker](https://www.docker.com/get-started) instalado en tu sistema.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado en tu sistema.

**Pasos:**

1.  Clona el repositorio del proyecto a tu máquina local.
2.  Navega al directorio raíz del proyecto (`microondas_flask`) en tu terminal.
3.  Ejecuta el siguiente comando para construir y levantar la aplicación:

    ```bash
    docker-compose up -d --build
    ```

4.  Una vez que los contenedores estén en funcionamiento, abre tu navegador web y ve a la siguiente dirección:

    ```
    http://localhost:5000/ // o en el puerto que hayas decidido redirigirlo
    ```

5.  Para detener la aplicación, ejecuta el siguiente comando en la misma terminal:

    ```bash
    docker-compose down // o CTRL + C en su defecto
    ```

### Opción 2: Despliegue con Entorno Virtual (venv)

Este método requiere tener Python y pip instalados en tu sistema.

**Prerequisites:**

* [Python 3](https://www.python.org/downloads/) instalado en tu sistema.
* `pip` (el gestor de paquetes de Python) instalado.

**Pasos:**

1.  Clona el repositorio del proyecto a tu máquina local.
2.  Navega al directorio raíz del proyecto (`microondas_flask`) en tu terminal.
3.  Crea un entorno virtual:

    ```bash
    python -m venv venv
    ```

4.  Activa el entorno virtual:
    * **En Windows:**

        ```bash
        .\venv\Scripts\activate
        ```
    * **En macOS y Linux:**

        ```bash
        source venv/bin/activate
        ```

5.  Instala las dependencias necesarias desde el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

6.  Ejecuta la aplicación Flask:

    ```bash
    python app.py
    ```

7.  Abre tu navegador web y ve a la siguiente dirección según el puerto que este abierto.