import pandas as pd
import logging

def interpolate_missing(df, numeric_cols=None):
    """
    Interpolate missing values within each station's time series.

    Args:
        df (pd.DataFrame): Input DataFrame with station data.
        numeric_cols (list, optional): List of numeric columns to interpolate.

    Returns:
        pd.DataFrame: DataFrame with interpolated values.
    """
    if "indicativo" not in df.columns:
        raise ValueError("Columna 'indicativo' faltante")
    if "fecha" not in df.columns:
        raise ValueError("Columna 'fecha' faltante")

    if numeric_cols is None:
        numeric_cols = ["tmin", "tmax", "tmed", "prec", "velmedia", "racha", "hrMedia"]

    def interpolate_group(grp, cols):
        grp = grp.sort_values('fecha').copy()
        available_cols = [col for col in cols if col in grp.columns]

        for col in available_cols:
            if 'start_date' in grp.columns and 'end_date' in grp.columns:
                start_date = grp['start_date'].iloc[0] if pd.notna(grp['start_date'].iloc[0]) else grp['fecha'].min()
                end_date = grp['end_date'].iloc[0] if pd.notna(grp['end_date'].iloc[0]) else grp['fecha'].max()
                active_mask = (grp['fecha'] >= start_date) & (grp['fecha'] <= end_date)
            else:
                active_mask = pd.Series([True] * len(grp), index=grp.index)

            before = grp.loc[active_mask, col].isna().sum()
            grp.loc[active_mask, col] = grp.loc[active_mask, col].interpolate(
                method='linear', limit=7, limit_direction='both'
            )
            after = grp.loc[active_mask, col].isna().sum()

            if before > after:
                logging.info(f"[{grp['indicativo'].iloc[0]}] Interpolated {before - after} values in '{col}'")

        return grp

    try:
        result = (
            df.groupby('indicativo', group_keys=False)
              .apply(lambda g: interpolate_group(g, numeric_cols))
              .reset_index(drop=True)
        )
        logging.info("Interpolación completada")
        return result
    except Exception as e:
        logging.error(f"Error durante interpolación: {e}")
        return df