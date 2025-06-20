import pandas as pd
import logging

def add_lat_lon(df, estaciones_path="C:\Repos\Augusto\data\estaciones.csv"):
    """
    Add latitude, longitude, and optionally start_date, end_date from estaciones.csv.
    
    Args:
        df (pd.DataFrame): Input DataFrame with 'indicativo' column.
        estaciones_path (str): Path to stations CSV file.
    
    Returns:
        pd.DataFrame: DataFrame with added 'latitud_dd', 'longitud_dd', 'start_date', 'end_date' columns.
    
    Raises:
        ValueError: If 'indicativo' column is missing or unmatched stations.
        FileNotFoundError: If estaciones file is not found.
    """
    if "indicativo" not in df.columns:
        raise ValueError("Columna 'indicativo' faltante")
    try:
        estaciones = pd.read_csv(estaciones_path)
        cols = ['indicativo', 'latitud_dd', 'longitud_dd']
        if 'start_date' in estaciones.columns and 'end_date' in estaciones.columns:
            cols.extend(['start_date', 'end_date'])
            estaciones['start_date'] = pd.to_datetime(estaciones['start_date'], errors='coerce')
            estaciones['end_date'] = pd.to_datetime(estaciones['end_date'], errors='coerce')
        coords = estaciones[cols]
        df = df.merge(coords, on='indicativo', how='left')
        unmatched = df[df['latitud_dd'].isna()]['indicativo'].unique()
        if len(unmatched) > 0:
            logging.warning(f"Estaciones sin coordenadas: {unmatched}")
            raise ValueError(f"Estaciones sin coordenadas en estaciones.csv: {unmatched}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo de estaciones no encontrado: {estaciones_path}")