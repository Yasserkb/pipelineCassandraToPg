import pandas as pd
from etl.logger import get_logger

import argparse
from etl.transform import normalize_categories
from etl.loader import load_table

logger = get_logger(__name__)


def standardize_columns():
    # Step 1: Load CSVs
    # TODO: Method that would loop over each directory and load data into the pg database
    users = pd.read_csv('cassandra_exports/users.csv')
    products = pd.read_csv('cassandra_exports/products.csv')
    orders = pd.read_csv('cassandra_exports/orders.csv')
    order_items = pd.read_csv('cassandra_exports/order_items.csv')

    # Step 2: Rename ID columns to match PostgreSQL schema
    users.rename(columns={'user_id': 'id'}, inplace=True)
    products.rename(columns={'product_id': 'id'}, inplace=True)
    orders.rename(columns={'order_id': 'id'}, inplace=True)

    # Step 3: Transform products & categories
    categories, products = normalize_categories(products)

    return users, categories, products, orders, order_items

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline: Cassandra → PostgreSQL")
    parser.add_argument('--dry-run', action='store_true', help='Transform but don’t insert into PostgreSQL')
    args = parser.parse_args()

    logger.info("🚀 Pipeline starting...")
    users, categories, products, orders, order_items = standardize_columns()

    if not args.dry_run:
        logger.info("📥 Loading to PostgreSQL...")
        load_table(users, "users")
        load_table(categories, "categories")
        load_table(products, "products")
        load_table(orders, "orders")
        load_table(order_items, "order_items")

