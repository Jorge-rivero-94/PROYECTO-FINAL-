import logging
from sqlalchemy import create_engine
import conectar

def order_load(df):
    """
    Reorder columns and insert data into SQL database.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: Input DataFrame (unchanged).
    
    Raises:
        ValueError: If required columns are missing.
        RuntimeError: If SQL insertion fails.
    """
    orden_columnas = [
        "id_descarga", "fecha", "indicativo", "nombre",
        "altitud", "tmed", "tmin", "tmax", "prec", "velmedia", "racha",
        "hrMedia", "timestamp_extraccion", "codigo_prov"
    ]
    missing_cols = [col for col in orden_columnas if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas requeridas faltantes: {missing_cols}")
    
    valores_insertar = df[orden_columnas]
    try:
        logging.info(f"Iniciando inserción de {len(valores_insertar)} filas...")
        valores_insertar.to_sql(
            name="datos_meteorologicos",
            con=conectar.conexion(),
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )
        logging.info(f"¡{len(valores_insertar)} filas insertadas correctamente!")
    except Exception as e:
        raise RuntimeError(f"Error durante la inserción: {e}")
    return df