import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Lee el archivo CSV
data = pd.read_csv("muestra.csv")

# Codifica la variable objetivo
encoder = LabelEncoder()
data['label_codificado'] = encoder.fit_transform(data['label'])

# Crea un mapeo para decodificar
mapeo_etiquetas = dict(zip(encoder.transform(encoder.classes_), encoder.classes_))
#Se imprimen los cambios de las etiquetas
print("Mapeo de etiquetas:")
print(mapeo_etiquetas)

# Separa características (X) y variable objetivo codificada (y)
X = data.drop(columns=["label", "label_codificado"])  # Todas las columnas excepto la columna objetivo
y = data["label_codificado"]  # Columna objetivo codificada

# Calcular la información mutua para todas las características
mi_scores = mutual_info_classif(X, y)

# Crea un DataFrame para mostrar las puntuaciones de información mutua
mi_df = pd.DataFrame({'Caracteristica': X.columns, 'Informacion_Mutua': mi_scores})

# Ordena las puntuaciones por información mutua de forma descendente
mi_df = mi_df.sort_values(by='Informacion_Mutua', ascending=False)

# Guarda las puntuaciones de información mutua en un archivo CSV
mi_df.to_csv('informacion_mutua.csv', index=False)

# Ajusta SelectKBest a los datos para seleccionar las 10 mejores características
seleccion = SelectKBest(mutual_info_classif, k=10)
X_seleccionado = seleccion.fit_transform(X, y)

# Obtener los nombres de las características seleccionadas
mascara_seleccion = seleccion.get_support()
caracteristicas_seleccionadas_nombres = X.columns[mascara_seleccion]

# Imprime los nombres de las características seleccionadas
print("Características seleccionadas por SelectKBest:")
for caracteristica in caracteristicas_seleccionadas_nombres:
    print(caracteristica)


#ENTRENAMIENTO#

# Divide los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_seleccionado, y, test_size=0.2, random_state=42)

# Entrena un modelo de clasificación (Árbol de decisión)
clasificador = DecisionTreeClassifier()
clasificador.fit(X_train, y_train)

# Realiza predicciones en el conjunto de prueba
y_pred = clasificador.predict(X_test)

# Decodifica las predicciones
y_pred_decodificado = encoder.inverse_transform(y_pred)

# Genera un informe de clasificación
reporte = classification_report(y_test, y_pred)
print("Informe de Clasificación:")
print(reporte)

with open("informe_clasificacion.txt", "w") as file:
    file.write(reporte)

# Guarda X_test en un archivo CSV
pd.DataFrame(X_test, columns=caracteristicas_seleccionadas_nombres).to_csv('X_test.csv', index=False)

# Decodifica las predicciones en el conjunto de prueba para tener los nombres de las etiquetas
y_test_decodificado = encoder.inverse_transform(y_test)

# Guarda y_test en un archivo CSV con nombres de etiquetas
pd.DataFrame(y_test_decodificado, columns=['Etiqueta_Real']).to_csv('y_test.csv', index=False)

# Decodifica las predicciones en el conjunto de prueba para tener los nombres de las etiquetas predichas
y_pred_decodificado = encoder.inverse_transform(y_pred)

# Guardar y_pred en un archivo CSV con nombres de etiquetas predichas
pd.DataFrame(y_pred_decodificado, columns=['Prediccion']).to_csv('y_pred.csv', index=False)

# Combinar X_test, y_test y y_pred en un solo DataFrame
resultado = pd.concat([pd.DataFrame(X_test, columns=caracteristicas_seleccionadas_nombres),
                       pd.DataFrame(y_pred_decodificado, columns=['Prediccion'])], axis=1)

# Guardar el DataFrame combinado en un archivo CSV con nombres de etiquetas
resultado.to_csv('resultado.csv', index=False)

# Tomar una muestra del 0.5% del tamaño original del DataFrame resultado.csv
df_sample = resultado.sample(frac=0.005, random_state=42)

# Guardar la muestra en un archivo CSV con nombres de etiquetas
df_sample.to_csv('resultado_porcentaje.csv', index=False)

# Crear el gráfico de barras
plt.figure(figsize=(12, 8))
sns.barplot(x='Informacion_Mutua', y='Caracteristica', data=mi_df, palette='viridis')
plt.title('Puntuaciones de Información Mutua para todas las características')
plt.xlabel('Información Mutua')
plt.ylabel('Característica')
plt.tight_layout() 
plt.show()

# Generar y mostrar la matriz de confusión
cm = confusion_matrix(y_test_decodificado, y_pred_decodificado, labels=encoder.classes_)
plt.figure(figsize=(12, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.tight_layout()
plt.show()