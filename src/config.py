"""
config.py
---------
Configuración central del proyecto: rutas, constantes y listas de variables.
Todos los demás módulos importan desde aquí, por lo que cualquier cambio
(por ejemplo, el tamaño del dataset) se hace en un único lugar.
"""
from pathlib import Path

# ---------- Rutas ----------
RAIZ = Path(__file__).resolve().parents[1]
DIR_DATOS_RAW = RAIZ / "data" / "raw"
DIR_DATOS_PROC = RAIZ / "data" / "processed"
DIR_MODELOS = RAIZ / "models"
DIR_REPORTES = RAIZ / "reports"
DIR_FIGURAS = DIR_REPORTES / "figures"

ARCHIVO_DATASET = DIR_DATOS_RAW / "ocupacion_transporte_masivo.csv"
ARCHIVO_MODELO = DIR_MODELOS / "arbol_decision_ocupacion.joblib"
ARCHIVO_METRICAS = DIR_REPORTES / "metricas.json"
ARCHIVO_RESUMEN_DATOS = DIR_REPORTES / "resumen_datos.json"
ARCHIVO_REGLAS = DIR_REPORTES / "reglas_arbol.txt"

# ---------- Parámetros generales ----------
SEMILLA = 42            # garantiza resultados reproducibles
N_REGISTROS = 3000      # tamaño del dataset sintético
TAM_PRUEBA = 0.20       # 20 % de los datos para prueba
VALIDACION_CRUZADA = 5  # número de pliegues en GridSearchCV

# ---------- Variables ----------
COLUMNA_ID = "id_registro"
COLUMNA_OBJETIVO = "nivel_ocupacion"
CLASES = ["Baja", "Media", "Alta"]

VARIABLES_NUMERICAS = ["hora", "temperatura_c", "buses_en_servicio", "frecuencia_min"]
VARIABLES_BINARIAS = ["es_festivo", "evento_masivo"]
VARIABLES_CATEGORICAS = ["dia_semana", "estacion", "tipo_zona", "clima"]
VARIABLES_PREDICTORAS = VARIABLES_NUMERICAS + VARIABLES_BINARIAS + VARIABLES_CATEGORICAS
COLUMNAS_DATASET = [COLUMNA_ID] + VARIABLES_PREDICTORAS + [COLUMNA_OBJETIVO]

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
ESTACIONES = {
    "Portal Norte": "Terminal",
    "Portal Sur": "Terminal",
    "Centro": "Comercial",
    "Centro Comercial": "Comercial",
    "Universidades": "Universitaria",
    "Zona Industrial": "Industrial",
    "Barrio Residencial": "Residencial",
    "Hospital": "Comercial",
}
CLIMAS = ["Soleado", "Nublado", "Lluvia"]


def crear_directorios() -> None:
    """Crea las carpetas de salida si no existen."""
    for carpeta in (DIR_DATOS_RAW, DIR_DATOS_PROC, DIR_MODELOS, DIR_FIGURAS):
        carpeta.mkdir(parents=True, exist_ok=True)
