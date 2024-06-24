# TFG: Desarrollo de un sistema de análisis y gestión de riesgos en entornos IoT.

En este Trabajo Fin de Grado se desarrolla un sistema de análisis y gestión de riesgos, basandose en el preprocesado de datos, selección de características, entrenamiento de un modelo de aprendizaje automático y ontologías. A continuación se detalla el orden y la función de cada uno de los ficheros.

**Fichero 1: unir.py**
Este fichero se encarga de unir los archivos csv necesarios para tener una muestra lo suficientemente grande para entrenar al modelo posteriormente,

**Fichero 2: filtro.py**
Este fichero se encarga de pre procesar los datos del fichero generado por unir.py, para posteriormente, seleccionar las características más relevantes mediante la información mutua y por último entrenar un modelo de aprendizaje automático, en este caso, un árbol de decisión. Además genera un informe de clasificación y una matriz de confusión con el fin de poder evaluar el rendimiento del modelo entrenado.

**Fichero 3: ontología.py**
Este fichero se encarga de recrear el escenario propuesto por el datase con el que se haya llevado a cabo el proyecto, en él se encuentran definidos todos los activos que el dataset, así como todo el código para cargar incidentes. a partir de estos incidentes que se encuentran en el fichero generado por filtro.py, se generan las amenazas y riesgos correspondientes. Se calcula el riesgo total y residual del sistema y se propone la aplicación de contramedidas.

**Fichero 4: casodeuso.py**
Este fichero es una particularización del anterior. Se trata del ejemplo que se muestra en el Capítulo 5 del TFG, concretamente el apartado 5.2. Aquí encontramos una selección de algunos activos y se cargan 2006 incidentes. De esta manera, contamos con una muestra más pequeña en la que se puede analizar bien el funcionamiento de la ontología.

**Entorno de ejecución**
Para ejecutar este proyecto, lo primero es descargar el dataset que se menciona en la memoria. Una vez descargado, hay que identificar la carpeta "CICIoT2023", que es donde se encuentran los archivos csv. Para ejecutar el proyecto basta con crear un directorio, e insertar en el la carpeta descargada y los ficheros python.
