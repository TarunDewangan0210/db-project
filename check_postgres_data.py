import psycopg2
import os
import pandas as pd

# Database connection settings
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "ecommerce_db"
PG_USER = "postgres"
PG_PASSWORD = "postgres"

# Get the absolute path of the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "eep-db-storage")

def check_csv_files():
    """Check if CSV files exist and show their contents"""
    csv_files = {
        'customers.csv': os.path.join(DATA_DIR, 'customers.csv'),
        'products.csv': os.path.join(DATA_DIR, 'products.csv'),
        'orders.csv': os.path.join(DATA_DIR, 'orders.csv'),
        'orderdtl.csv': os.path.join(DATA_DIR, 'orderdtl.csv')
    }
    
    for file_name, file_path in csv_files.items():
        print(f"\nChecking {file_name}:")
        if os.path.exists(file_path):
            print(f"File exists at: {file_path}")
            try:
                df = pd.read_csv(file_path)
                print(f"Number of rows: {len(df)}")
                print("\nFirst 5 rows:")
                print(df.head())
            except Exception as e:
                print(f"Error reading file: {str(e)}")
        else:
            print(f"File not found at: {file_path}")

def check_table_data():
    """Check data in all tables"""
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    tables = ['customers', 'products', 'orders', 'order_details']
    
    for table in tables:
        print(f"\nChecking {table} table:")
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"Total records: {count}")
        
        if count > 0:
            cur.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = cur.fetchall()
            print("\nSample data:")
            for row in rows:
                print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    print("Checking CSV files...")
    check_csv_files()
    
    print("\nChecking database tables...")
    check_table_data() 