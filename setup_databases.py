import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import sys
import time

# Load environment variables
load_dotenv()

# Get the absolute path of the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "eep-db-storage")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# PostgreSQL connection
PG_HOST = "localhost"
PG_PORT = "5433"
PG_DB = "ecommerce_db"
PG_USER = "postgres"
PG_PASSWORD = "postgres"

# MongoDB connection
MONGO_URI = "mongodb://admin:admin@localhost:27018/admin?authSource=admin"  # Hardcoded URI to prevent override
MONGO_DB = "ecommerce_analytics"

def check_required_files():
    """Check if all required files exist and print their status"""
    required_files = {
        'customers.csv': os.path.join(DATA_DIR, 'customers.csv'),
        'products.csv': os.path.join(DATA_DIR, 'products.csv'),
        'orders.csv': os.path.join(DATA_DIR, 'orders.csv'),
        'orderdtl.csv': os.path.join(DATA_DIR, 'orderdtl.csv'),
        'web_traffic.json': os.path.join(PROJECT_DIR, 'web_traffic.json')
    }
    
    missing_files = []
    for file_name, file_path in required_files.items():
        if not os.path.exists(file_path):
            missing_files.append(file_name)
            print(f"Missing file: {file_name}")
        else:
            print(f"Found file: {file_name}")
    
    if missing_files:
        print("\nPlease ensure the following files are present:")
        for file in missing_files:
            print(f"- {file}")
        print(f"\nExpected locations:")
        print(f"CSV files should be in: {DATA_DIR}")
        print(f"web_traffic.json should be in: {PROJECT_DIR}")
        return False
    return True

def setup_postgres_tables():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()

    # Drop existing tables if they exist
    cur.execute("""
        DROP TABLE IF EXISTS order_details;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
    """)

    # Create tables with correct structure
    cur.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(100),
            price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            order_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE order_details (
            line_num INTEGER PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    return conn, cur

def load_csv_data(conn, cur, csv_dir):
    try:
        # Load customers
        customers_file = os.path.join(csv_dir, "customers.csv")
        if not os.path.exists(customers_file):
            raise FileNotFoundError(f"Customers CSV file not found at {customers_file}")
        
        customers_df = pd.read_csv(customers_file)
        print("\nCustomers CSV columns:", customers_df.columns.tolist())
        
        for _, row in customers_df.iterrows():
            cur.execute("""
                INSERT INTO customers (customer_id, name, email, address)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (customer_id) DO NOTHING
            """, (int(row['customer_id']), str(row['name']), str(row['email']), str(row['address'])))

        # Load products
        products_file = os.path.join(csv_dir, "products.csv")
        if not os.path.exists(products_file):
            raise FileNotFoundError(f"Products CSV file not found at {products_file}")
        
        products_df = pd.read_csv(products_file)
        print("\nProducts CSV columns:", products_df.columns.tolist())
        
        for _, row in products_df.iterrows():
            cur.execute("""
                INSERT INTO products (product_id, name, category, price)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING
            """, (int(row['product_id']), str(row['name']), str(row['category']), float(row['price'])))

        # Load orders
        orders_file = os.path.join(csv_dir, "orders.csv")
        if not os.path.exists(orders_file):
            raise FileNotFoundError(f"Orders CSV file not found at {orders_file}")
        
        orders_df = pd.read_csv(orders_file)
        print("\nOrders CSV columns:", orders_df.columns.tolist())
        
        for _, row in orders_df.iterrows():
            cur.execute("""
                INSERT INTO orders (order_id, customer_id, order_date)
                VALUES (%s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
            """, (int(row['order_id']), int(row['customer_id']), str(row['order_date'])))

        # Load order details
        orderdtl_file = os.path.join(csv_dir, "orderdtl.csv")
        if not os.path.exists(orderdtl_file):
            raise FileNotFoundError(f"Order details CSV file not found at {orderdtl_file}")
        
        orderdtl_df = pd.read_csv(orderdtl_file)
        print("\nOrder details CSV columns:", orderdtl_df.columns.tolist())
        
        for _, row in orderdtl_df.iterrows():
            cur.execute("""
                INSERT INTO order_details (line_num, order_id, product_id, quantity)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (line_num) DO NOTHING
            """, (int(row['line_num']), int(row['order_id']), int(row['product_id']), int(row['quantity'])))

        conn.commit()
        print("\nData loaded successfully!")
        
    except Exception as e:
        print(f"\nError loading data: {str(e)}")
        conn.rollback()
        raise

def setup_mongodb():
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"\nAttempting MongoDB connection (Attempt {attempt + 1}/{max_retries})")
            print(f"Connection URI: {MONGO_URI}")
            
            # Connect to MongoDB with authentication in URI
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
            # Get the database
            db = client[MONGO_DB]
            
            # Create web_traffic collection if it doesn't exist
            if 'web_traffic' not in db.list_collection_names():
                db.create_collection('web_traffic')
                print("Created web_traffic collection")
            
            # Load web traffic data
            web_traffic_file = os.path.join(PROJECT_DIR, 'web_traffic.json')
            if not os.path.exists(web_traffic_file):
                raise FileNotFoundError(f"Web traffic JSON file not found at {web_traffic_file}")
            
            # Read and parse JSONL file
            web_traffic_data = []
            with open(web_traffic_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        web_traffic_data.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Skipping invalid JSON line: {e}")
                        continue
            
            if web_traffic_data:
                # Insert data in batches
                batch_size = 1000
                for i in range(0, len(web_traffic_data), batch_size):
                    batch = web_traffic_data[i:i + batch_size]
                    db.web_traffic.insert_many(batch)
                print(f"Successfully loaded {len(web_traffic_data)} web traffic records")
            else:
                print("No valid web traffic data found to load")
            
            return client
            
        except Exception as e:
            print(f"Error connecting to MongoDB (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to MongoDB.")
                raise

def create_indexes():
    # PostgreSQL indexes
    conn, cur = setup_postgres_tables()
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
        CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON order_details(order_id);
        CREATE INDEX IF NOT EXISTS idx_order_details_product_id ON order_details(product_id);
        CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    
    # MongoDB indexes
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"\nAttempting to create MongoDB indexes (Attempt {attempt + 1}/{max_retries})")
            
            # Connect to MongoDB with authentication in URI
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection with explicit error handling
            try:
                print("Testing connection with ping command...")
                client.admin.command('ping')
                print("Successfully connected to MongoDB")
            except Exception as e:
                print(f"Failed to ping MongoDB: {str(e)}")
                raise
            
            # Now switch to our database
            print(f"Switching to database: {MONGO_DB}")
            db = client[MONGO_DB]
            web_traffic = db.web_traffic
            
            # Create indexes with explicit options
            try:
                print("Creating indexes...")
                web_traffic.create_index([("timestamp", 1)], background=True)
                web_traffic.create_index([("product_id", 1)], background=True)
                web_traffic.create_index([("user_id", 1)], background=True)
                print("MongoDB indexes created successfully")
            except Exception as e:
                print(f"Error creating indexes: {str(e)}")
                raise
                
            break
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not create MongoDB indexes.")
                raise

def main():
    try:
        print("Checking required files...")
        if not check_required_files():
            print("\nPlease add the missing files and run the script again.")
            sys.exit(1)
            
        print("\nSetting up PostgreSQL tables...")
        conn, cur = setup_postgres_tables()
        
        print("\nLoading data from CSV files...")
        load_csv_data(conn, cur, DATA_DIR)
        cur.close()
        conn.close()
        
        print("\nSetting up MongoDB...")
        client = setup_mongodb()
        
        print("\nCreating indexes...")
        create_indexes()
        
        print("\nDatabase setup completed successfully!")
        
    except Exception as e:
        print(f"\nError in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 