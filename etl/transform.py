import pandas as pd
from pandas import DataFrame
from etl.logger import get_logger

logger = get_logger(__name__)

def normalize_categories(products_df: DataFrame) -> tuple[DataFrame, DataFrame]:
    if 'category' not in products_df.columns:
        logger.error("❌ 'category' column is missing from products dataframe.")
        raise ValueError("Missing required 'category' column in products DataFrame.")

    try:
        unique_categories = products_df['category'].dropna().unique()
        category_df = pd.DataFrame(unique_categories, columns=['name'])
        category_df['id'] = range(1, len(category_df) + 1)

        category_map = dict(zip(category_df['name'], category_df['id']))
        products_df['category_id'] = products_df['category'].map(category_map)

        logger.info(f"✅ Normalized {len(category_df)} product categories.")
        return category_df[['id', 'name']], products_df.drop(columns=['category'])

    except Exception as e:
        logger.exception("❌ Failed to normalize product categories.")
        raise