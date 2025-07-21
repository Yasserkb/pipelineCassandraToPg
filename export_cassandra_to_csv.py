from cassandra.cluster import Cluster
import pandas as pd
import os

cluster = Cluster(['127.0.0.1'], port=9042)  # or use your docker IP
session = cluster.connect('db1')  # keyspace

output_dir = 'cassandra_exports'
os.makedirs(output_dir, exist_ok=True)

def export_to_csv(query, filename):
    rows = session.execute(query)
    df = pd.DataFrame(rows.all())
    if not df.empty:
        df.to_csv(os.path.join(output_dir, filename), index=False)
        print(f"✅ Exported {filename} ({len(df)} rows)")
    else:
        print(f"⚠️  No data found for {filename}")

export_to_csv("SELECT * FROM users;", "users.csv")
export_to_csv("SELECT * FROM products;", "products.csv")
export_to_csv("SELECT * FROM orders;", "orders.csv")
export_to_csv("SELECT * FROM order_items;", "order_items.csv")

cluster.shutdown()
