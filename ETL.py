import os
from Extract.hacer_peticion import extraer_ultimos_tres_dias
from Clean.clean_timestamp import clean_timestamps
from Clean.standarize_provinces import standardize_provinces
from Clean.convert_types import convert_types
from Clean.engineer_calendar_features import engineer_calendar_features
from Clean.filter_physical_outliers import filter_physical_outliers
from Clean.interpolate_missing import interpolate_missing
from Clean.add_info import add_info
from Clean.knn_impute import knn_impute
from Clean.order import order
#from poblar import poblar
import logging
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_data():
    """Extract data using provided functions."""
    try:
        logger.info("Starting extraction process")
        df = extraer_ultimos_tres_dias()
        extract_path = "data/extract.pkl"
        os.makedirs("data", exist_ok=True)
        df.to_pickle(extract_path)
        logger.info(f"Extracted data saved to {extract_path} ")
        logger.info(f"Extracted {len(df)} rows")
        return df.copy()
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise

def transform_data(df):
    """Transform the extracted data through multiple steps."""
    try:
        logger.info("Starting transformation process")
        df = clean_timestamps(df)
        logger.info("Timestamps cleaned")
        
        df = standardize_provinces(df, mapping_path="data/mapa_provincia.json")
        logger.info("Provinces standardized")
        
        df = convert_types(df, numeric_cols=None)
        logger.info("Data types converted")
        
        df = engineer_calendar_features(df)
        logger.info("Calendar features engineered")
        
        df = filter_physical_outliers(df)
        logger.info("Physical outliers filtered")
        
        df = interpolate_missing(df, numeric_cols=None)
        logger.info("Missing values interpolated")
        
        df = add_info(df, estaciones_path="data/estaciones_nombre_indicativo.csv")
        logger.info("Additional info added")
        
        df = knn_impute(df, numeric_cols=None)
        logger.info("KNN imputation completed")
        
        df = order(df)
        logger.info("Data ordered")
        
        return df
    except Exception as e:
        logger.error(f"Error during transformation: {e}")
        raise

#función poblar aqui

def run_etl(save_path=r"C:\Users\User\OneDrive - Universidade de Santiago de Compostela\Documentos\Data Science\Data Science & IA Bootcamp 2024\PFB\Sprint_II\notebooks\Final\output.pkl"):
    """Run the complete ETL pipeline and save to pickle."""
    try:
        # Extract
        #df = extract_data()

        df = pd.read_pickle("data/extract.pkl")
   
        # Transform
        df_transformed = transform_data(df)
        
        # Load
        #poblar(df_transformed)

        # Save to pickle
        df_transformed.to_pickle(save_path)
        logger.info(f"DataFrame saved to {save_path}")
        
        logger.info("ETL pipeline completed successfully")
        return df_transformed
    except Exception as e:
        logger.error(f"Error in ETL pipeline: {e}")
        raise

if __name__ == "__main__":
    run_etl()