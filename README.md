# Knight Energy
Un juego de estrategia construido con **Pygame** que permite la interacción y competencia por turnos con un IA que emplea el algoritmo MinMax junto con una función heurística.

## Características
* **Algoritmo MinMax:** Que selecciona la mejor jugada hasta una profundidad dada.
* **Dificultad variable:** Selecciona entre Principiante, Amateur y Experto para variar la profundidad máxima de búsqueda del algoritmo.
* **Interfaz Gráfica:** Interacción completa por medio de interfaz visual construida en pygame. 

## Requisitos Previos
Asegúrate de tener instalado [Python](https://www.python.org/downloads/) en tu sistema. (Se recomienda una versión estable como **Python 2.6.1**).

## Instalación y Ejecución
Sigue estos pasos para clonar y ejecutar el proyecto en tu máquina local de forma segura utilizando un entorno virtual.

### 1. Clonar el repositorio
Abre tu terminal y ejecuta: 
```bash
git clone https://github.com/18luisc/Knight_Energy
```
### 2. Crear un entorno virtual
Para evitar conflictos con otras librerías de tu sistema, crea un entorno virtual (venv):
```bash
python -m venv venv
```
O en algunos equipos:
```bash
py -m venv venv
```

### 3. Activar el entorno virtual
* **En Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
* **En macOS y Linux:**
  ```bash
  source venv/bin/activate
  ```
### 4. Instalar las dependencias
Con el entorno activado, instala la versión de Pygame requerida:
```bash
pip install -r requirements.txt
```

### 5. Iniciar la simulación
Finalmente, navega hasta la carpeta de código y ejecuta el archivo principal 
```bash
python main.py
```
O:
```bash
py main.py
```

## Cómo usar
1. Al iniciar, selecciona tu dificultad deseada entre **Principiante, Amateur o Experto**
2. Haz click al interior del tablero para iniciar el juego, la máquina (blancas) realizan la primer jugada.
3. En tu turno, haz click sobre la casilla a la cual desear moverte, si es una casilla válida tu ficha se moverá.
4. Juega hasta que ambos jugadores se queden sin energía, o hasta que todos los puntos hayan sido recogidos. ¡Buena suerte!
