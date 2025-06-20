import json

def standardize_provinces(df, mapping_path="data/mapa_provincia.json"):
    """
    Standardize province names using a JSON mapping file.
    
    Args:
        df (pd.DataFrame): Input DataFrame with 'provincia' column.
        mapping_path (str): Path to JSON mapping file.
    
    Returns:
        pd.DataFrame: DataFrame with standardized 'provincia' column.
    
    Raises:
        ValueError: If 'provincia' column is missing or JSON is invalid.
        FileNotFoundError: If mapping file is not found.
    """
    if "provincia" not in df.columns:
        raise ValueError("Columna 'provincia' faltante")
    try:
        with open(mapping_path, "r", encoding="utf-8") as f:
            mapa_provincias = json.load(f)
        df["provincia"] = df["provincia"].map(mapa_provincias).fillna(df["provincia"])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo de mapeo no encontrado: {mapping_path}")
    except json.JSONDecodeError:
        raise ValueError(f"JSON inválido en el archivo: {mapping_path}")