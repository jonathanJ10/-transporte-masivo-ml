# Clasificación de la ocupación en transporte masivo con aprendizaje supervisado

Proyecto de la asignatura **Inteligencia Artificial** (Ingeniería de Software, Universidad Iberoamericana).
Un **árbol de decisión** predice el nivel de ocupación (**Baja, Media o Alta**) de una estación de un sistema de transporte masivo a partir de la hora, el día, el clima, la zona, los eventos y la oferta de buses.

## Integrantes

| Integrante | Rol principal |
|---|---|
| Johathan Granobles Penagos | Datos y generación del dataset |
| [Integrante 2] | Preprocesamiento y entrenamiento |
| [Integrante 3] | Evaluación, pruebas y documentación |

Docente: William Ruiz.

## Estructura del proyecto

```
transporte-masivo-ml/
├── main.py                  # Ejecuta todo el flujo
├── requirements.txt         # Librerías necesarias
├── pytest.ini
├── data/
│   ├── raw/ocupacion_transporte_masivo.csv   # Dataset (3000 registros)
│   └── processed/
├── src/
│   ├── config.py            # Rutas, constantes y variables
│   ├── generar_dataset.py   # Crea el dataset sintético
│   ├── explorar_datos.py    # Análisis exploratorio y gráficos
│   ├── preprocesamiento.py  # Carga, validación, división e imputación
│   ├── entrenar_modelo.py   # Árbol de decisión + GridSearchCV
│   ├── evaluar_modelo.py    # Métricas, matriz de confusión, reglas
│   └── predecir.py          # Predicción de casos nuevos
├── tests/test_pipeline.py   # 15 pruebas automatizadas
├── models/                  # Modelo entrenado (.joblib)
├── reports/                 # Métricas, reglas y figuras
└── docs/                    # Documentos Word/PDF de la entrega
```

## Cómo ejecutarlo

```bash
# 1. Clonar el repositorio
git clone https://github.com/<usuario>/transporte-masivo-ml.git
cd transporte-masivo-ml

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Ejecutar el flujo completo
python main.py

# 4. Ejecutar las pruebas
python -m pytest -v

# 5. (Opcional) Predecir casos de ejemplo con el modelo guardado
python -m src.predecir
```

Para volver a crear el dataset desde cero: `python main.py --regenerar`.

## Resultados (conjunto de prueba, 600 registros)

Ver `reports/metricas.json` y el documento `docs/` correspondiente. La semilla fija (`SEMILLA = 42`) hace que los resultados sean reproducibles.

## Nota sobre los datos

No se encontró una fuente abierta con todas las variables requeridas, por lo que el dataset es **sintético**. Sus reglas de simulación están documentadas en `src/generar_dataset.py` y en el documento de descripción de los datos.
