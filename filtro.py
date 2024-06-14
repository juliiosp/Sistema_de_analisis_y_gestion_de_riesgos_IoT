import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Leemos el archivo CSV
data = pd.read_csv("muestra.csv")

# Separamos las características (X) a analizar del objetivo (y)
X = data.drop(columns=["label"])  # Todas las columnas excepto la columna objetivo
y = data["label"]   # Columna objetivo

# Calculamos la información mutua entre cada característica y el objetivo
# Ajustar SelectKBest a tus datos
seleccion = SelectKBest(mutual_info_classif, k=10)
caracteristicas_seleccionadas = seleccion.fit_transform(X, y)

# Obtener la máscara de características seleccionadas
mascara_seleccion = seleccion.get_support()

# Obtener los nombres de las características seleccionadas
caracteristicas_seleccionadas_nombres = X.columns[mascara_seleccion]

# Imprimo los nombres de las características seleccionadas para después poder nombrarlos en el archivo nuevo
print("Características seleccionadas por SelectKBest:")
for caracteristica in caracteristicas_seleccionadas_nombres:
    print(caracteristica)

# Dividimos los datos en dos conjuntos: entrenamiento y validación
X_train, X_test, y_train, y_test = train_test_split(caracteristicas_seleccionadas, y, test_size=0.2, random_state=42)

# Entrenamos un modelo de clasificación (Árbol de decisión)
clasificador = DecisionTreeClassifier()
clasificador.fit(X_train, y_train)

# Realizamos predicciones en el conjunto de prueba
y_pred = clasificador.predict(X_test)
report = classification_report(y_test, y_pred)

# Imprimimos un informe de clasificación
# TP = verdaderos positivos // FP = falsos positivos // FN = falsos negativos // TN = verdaderos negativos
# Precision: proporción de instancias clasificadas como positivas que son verdaderamente positivas.Se calcula como TP / (TP + FP).
# Recall: proporción de instancias positivas que fueron correctamente detectadas por el clasificador. Se calcula como TP / (TP + FN).
# F1-score: media armónica de precisión y recall. Se calcula como  2 * (precision * recall) / (precision + recall).
# Support: número de instancias de la clase objetivo en los datos de prueba.
# Accuracy: proporción de instancias clasificadas correctamente entre todas las instancias. Se calcula como (TP + TN) / (TP + TN + FP + FN)
# Macro avg: media aritmética de las métricas para cada clase.
# Weighted avg: promedio ponderado de las métricas para cada clase, donde el peso es el soporte de cada clase.

# Guardar el informe de clasificación en un archivo de texto
with open("informe_clasificacion.txt", "w") as file:
    file.write(report)

# Generar y mostrar la matriz de confusión
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(12, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=y.unique(), yticklabels=y.unique())
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()

# Guardar X_test en un archivo CSV
pd.DataFrame(X_test).to_csv('X_test.csv', index=False)
# Guardar y_pred en un archivo CSV
pd.DataFrame(y_pred).to_csv('y_pred.csv', index=False)

# Cargamos los archivos CSV con nombres de columnas
archivo1 = pd.read_csv('X_test.csv', names=['Header_Length', 'Protocol_Type', 'Srate', 'Tot_Sum', 'Min', 'Max', 'AVG', 'Tot_Size', 'IAT', 'Magnitue'])
archivo2 = pd.read_csv('y_pred.csv', names=['Predicción'])

# Unimos los archivos
resultado = pd.concat([archivo1, archivo2], axis=1)

# Guardamos el resultado en un nuevo archivo CSV
resultado.to_csv('resultado.csv', index=False)

# Leer el archivo CSV original
df = pd.read_csv("resultado.csv")

# Obtener el 0.1% del tamaño original del DataFrame
df_sample = df.sample(frac=0.001, random_state=42)

# Guardar el DataFrame recortado en un nuevo archivo CSV
output_csv = "resultado_porcentaje.csv"
df_sample.to_csv(output_csv, index=False)
