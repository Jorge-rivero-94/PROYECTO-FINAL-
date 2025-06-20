import logging
import pandas as pd
from sqlalchemy import create_engine
import conectar

def add_province_code(df):
    """
    Add province codes from a SQL database.
    
    Args:
        df (pd.DataFrame): Input DataFrame with 'provincia' column.
    
    Returns:
        pd.DataFrame: DataFrame with 'codigo_provincia' column.
    
    Raises:
        ValueError: If 'provincia' column is missing.
        RuntimeError: If SQL query fails.
    """
    if "provincia" not in df.columns:
        raise ValueError("Columna 'provincia' faltante")
    try:
        query = "SELECT codigo_prov AS codigo_provincia, nombre FROM provincias"
        provincias = pd.read_sql(query, con=conectar.conexion())
        provincias["nombre"] = provincias["nombre"].str.strip()
        df = df.merge(provincias, left_on="provincia", right_on="nombre", how="left")
        unmatched = df[df["codigo_provincia"].isna()]["provincia"].unique()
        if len(unmatched) > 0:
            logging.warning(f"Provincias sin código: {unmatched}")
        df.drop(columns=["nombre"], inplace=True)
        return df
    except Exception as e:
        raise RuntimeError(f"Query SQL falló: {e}")