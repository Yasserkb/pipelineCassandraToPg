from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pandas as pd

from etl.logger import get_logger

logger = get_logger(__name__)

load_dotenv()
PG_URI = os.getenv("POSTGRES_URI")
engine = create_engine(PG_URI)

def load_table(df: pd.DataFrame, table: str):
    try:
        df.to_sql(table, engine, if_exists='append', index=False)
        logger.info(f"✅ Loaded: {table} ({len(df)} rows)")
    except Exception as e:
        logger.error(f"❌ Failed to load {table}: {str(e)}", exc_info=True)

