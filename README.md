# Desarrollo de un sistema de análisis y gestión de riesgos en entornos IoT.

**Julio Sánchez-Pajares Aliseda**

**GITST - ETSIT UPM**

# Requisitos
Para ejecutar el siguiente código hay que instalar las siguientes librerías:
- Pandas
- Seaborn
- Matplotlib
- Owlready2
- Reportlab
- Scikit-learn

# Estructura

El repositorio cuenta con cuatro archivos Python, y cada uno de ellos realiza las siguientes funciones.

## Fichero 1: `unir.py`
Este fichero se encarga de unir los archivos CSV necesarios para tener una muestra lo suficientemente grande para entrenar al modelo posteriormente.

## Fichero 2: `filtro.py`
Este fichero se encarga de preprocesar los datos del fichero generado por `unir.py`, para posteriormente, seleccionar las características más relevantes mediante la información mutua y, por último, entrenar un modelo de aprendizaje automático, en este caso, un árbol de decisión. Además, genera un informe de clasificación y una matriz de confusión con el fin de poder evaluar el rendimiento del modelo entrenado.

## Fichero 3: `ontología.py`
Este fichero se encarga de recrear el escenario propuesto por el dataset con el que se haya llevado a cabo el proyecto. En él se encuentran definidos todos los activos presentes en el escenario del dataset, así como todo el código para cargar incidentes, generar las amenazas y riesgos correspondientes y aplicar contramedidas. 

## Fichero 4: `casodeuso.py`
Este fichero es una particularización del anterior. Se trata del ejemplo que se muestra en el Capítulo 5 del TFG, concretamente el apartado 5.2. Aquí encontramos una selección de algunos activos y se cargan 2006 incidentes. De esta manera, contamos con una muestra más pequeña en la que se puede analizar mejor el funcionamiento de la ontología.

# Ejecución

Para la ejecución del código es necesario, en primer lugar, la creación de un directorio con un nombre cualquiera. Posteriormente, se descargan los ficheros alojados en GitHub y se depositan en el directorio creado. Cabe mencionar que el archivo `casodeuso.py` es el usado para la validación mostrada en esta memoria, por lo que es opcional su ejecución.

En segundo lugar, se descarga el dataset y se deposita la carpeta `CICIoT2023`, que es donde se encuentran los ficheros CSV, en el directorio de trabajo. Por último, es necesario crear una ontología vacía. Para esto es suficiente con abrir Protégé, crear una ontología y guardarla, de manera que se cree en el directorio de trabajo un archivo `.rdf`. Así, el código podrá encontrar el archivo y cargar los datos.

Una vez creado el directorio de trabajo, se ejecuta:

```bash
> python3 unir.py
```
En este fichero se une el número de archivos csv indicados en el código, generando “muestra.csv”.
El siguiente paso es ejecutar:
```bash
> python3 filtro.py
```
Se preprocesan los datos, se calcula la información mutua y por último se entrena el árbol de decisión.
Finalmente, en el fichero ontología.py, modificando previamente la dirección del directorio donde se encuentre el archivo.rdf, tanto en la décima como última línea del código, se ejecuta:
```bash
> python3 ontología.py
```
Se carga la ontología en el archivo indicado y se genera un fichero PDF.
Si se abre el archivo.rdf con Protégé, se podrá observar las clases creadas, relaciones, atributos e instancias generadas.


