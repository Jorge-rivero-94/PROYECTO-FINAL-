import numpy as np
import pandas as pd

def engineer_calendar_features(df):
    """
    Add calendar-based features from the 'fecha' column.
    
    Args:
        df (pd.DataFrame): Input DataFrame with 'fecha' and 'indicativo' columns.
    
    Returns:
        pd.DataFrame: DataFrame with added calendar features.
    
    Raises:
        ValueError: If 'fecha' or 'indicativo' columns are missing.
    """
    if 'fecha' not in df.columns:
        raise ValueError("Sin columna 'fecha'")
    if 'indicativo' not in df.columns:
        raise ValueError("Sin columna 'indicativo'")
    
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.sort_values(["indicativo", "fecha"]).reset_index(drop=True)
    df['month'] = df['fecha'].dt.month
    df['day_of_year'] = df['fecha'].dt.dayofyear
    df['sin_day'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
    df['cos_day'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)
    
    df[['month', 'day_of_year', 'sin_day', 'cos_day']] = df[['month', 'day_of_year', 'sin_day', 'cos_day']].fillna(0)
    return df