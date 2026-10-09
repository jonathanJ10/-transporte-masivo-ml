"""
generar_dataset.py
------------------
Genera un dataset SINTÉTICO que simula registros de ocupación en estaciones
de un sistema de transporte masivo (tipo troncal de buses).

Se usa porque no se dispone de una fuente abierta con todas las variables
requeridas. Las reglas de simulación están inspiradas en el comportamiento
real: horas pico, fines de semana, lluvia, eventos masivos y oferta de buses.
"""
import numpy as np
import pandas as pd

from src import config as cfg


def _curva_demanda(hora: np.ndarray) -> np.ndarray:
    """Devuelve un factor de demanda (0.15 a 1.0) con picos a las 7 y 18 h."""
    pico_manana = np.exp(-((hora - 7) ** 2) / (2 * 1.3 ** 2))
    pico_tarde = np.exp(-((hora - 18) ** 2) / (2 * 1.6 ** 2))
    valle = 0.15
    return np.clip(valle + 0.85 * np.maximum(pico_manana, pico_tarde), 0, 1)


def generar_dataset(n: int = cfg.N_REGISTROS, semilla: int = cfg.SEMILLA) -> pd.DataFrame:
    """Crea el DataFrame sintético con n registros."""
    rng = np.random.default_rng(semilla)

    # --- Variables de contexto ---
    horas = np.arange(5, 23)  # servicio de 5:00 a 22:00
    pesos = _curva_demanda(horas) + 0.25
    hora = rng.choice(horas, size=n, p=pesos / pesos.sum())
    dia_idx = rng.integers(0, 7, size=n)
    dia_semana = np.array(cfg.DIAS_SEMANA)[dia_idx]
    es_festivo = (rng.random(n) < 0.04).astype(int)
    evento_masivo = (rng.random(n) < 0.06).astype(int)

    estacion = rng.choice(list(cfg.ESTACIONES.keys()), size=n)
    tipo_zona = np.array([cfg.ESTACIONES[e] for e in estacion])

    clima = rng.choice(cfg.CLIMAS, size=n, p=[0.45, 0.35, 0.20])
    temp_media = np.select([clima == "Soleado", clima == "Nublado"], [20, 16], default=13)
    temperatura_c = np.round(rng.normal(temp_media, 2.5), 1)

    # --- Oferta de servicio ---
    demanda = _curva_demanda(hora)
    buses = np.clip(np.round(14 + 14 * demanda + rng.normal(0, 3, n)), 8, 40).astype(int)
    frecuencia = np.clip(np.round(120 / buses + rng.normal(0, 0.5, n), 1), 1.5, 12.0)

    # --- Porcentaje de ocupación (variable oculta que define la clase) ---
    pct = 25 + 55 * demanda
    pct = pct * np.select([dia_semana == "Sábado", dia_semana == "Domingo"], [0.75, 0.60], default=1.0)
    pct = pct * np.where(es_festivo == 1, 0.70, 1.0)
    pct = pct + np.select(
        [tipo_zona == "Terminal", tipo_zona == "Comercial", tipo_zona == "Universitaria"],
        [8, 4, 3], default=0)
    pct = pct + np.select([clima == "Lluvia", clima == "Nublado"], [8, 2], default=0)
    pct = pct + 12 * evento_masivo
    pct = pct - 0.6 * (buses - 22) + 1.5 * (frecuencia - 6)
    pct = np.clip(pct + rng.normal(0, 3, n), 5, 100)

    nivel = np.select([pct < 45, pct < 75], ["Baja", "Media"], default="Alta")

    df = pd.DataFrame({
        cfg.COLUMNA_ID: np.arange(1, n + 1),
        "dia_semana": dia_semana,
        "hora": hora,
        "es_festivo": es_festivo,
        "estacion": estacion,
        "tipo_zona": tipo_zona,
        "clima": clima,
        "temperatura_c": temperatura_c,
        "evento_masivo": evento_masivo,
        "buses_en_servicio": buses,
        "frecuencia_min": frecuencia,
        cfg.COLUMNA_OBJETIVO: nivel,
    })

    # --- Valores faltantes simulados (para practicar el preprocesamiento) ---
    df.loc[rng.random(n) < 0.02, "temperatura_c"] = np.nan
    df.loc[rng.random(n) < 0.015, "clima"] = np.nan
    return df[cfg.COLUMNAS_DATASET]


def guardar_dataset(df: pd.DataFrame, ruta=cfg.ARCHIVO_DATASET) -> None:
    """Guarda el dataset en CSV (UTF-8)."""
    cfg.crear_directorios()
    df.to_csv(ruta, index=False, encoding="utf-8")


if __name__ == "__main__":
    datos = generar_dataset()
    guardar_dataset(datos)
    print(f"Dataset generado: {len(datos)} registros -> {cfg.ARCHIVO_DATASET}")
    print(datos[cfg.COLUMNA_OBJETIVO].value_counts())
