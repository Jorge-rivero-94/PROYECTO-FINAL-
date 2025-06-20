def order(df):
    """
    Reordenar columnas.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame con las columnas seleccionas
    
    Raises:
        ValueError: If required columns are missing.
    """
    orden_columnas = [
        "id_descarga", "fecha", "indicativo", "nombre", "provincia"
        "altitud", "tmed", "tmin", "tmax", "prec", "velmedia",
        "hrMedia", "timestamp_extraccion", "cluster"
    ]
    missing_cols = [col for col in orden_columnas if col in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas requeridas faltantes: {missing_cols}")
    
    valores_insertar = df[orden_columnas]
    return valores_insertar  # Return filtered DataFrame