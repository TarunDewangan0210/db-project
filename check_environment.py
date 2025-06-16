import sys
import os

def check_environment():
    print("Python Environment Check")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check required packages
    required_packages = ['pandas', 'psycopg2-binary', 'pymongo', 'python-dotenv']
    
    print("\nChecking required packages:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
    
    # Check file permissions
    print("\nChecking file permissions:")
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eep-db-storage")
    if os.path.exists(data_dir):
        print(f"✓ Data directory exists: {data_dir}")
        for file in ['customers.csv', 'products.csv', 'orders.csv', 'orderdtl.csv']:
            file_path = os.path.join(data_dir, file)
            if os.path.exists(file_path):
                print(f"✓ {file} exists")
                if os.access(file_path, os.R_OK):
                    print(f"✓ {file} is readable")
                else:
                    print(f"✗ {file} is NOT readable")
            else:
                print(f"✗ {file} does NOT exist")
    else:
        print(f"✗ Data directory does NOT exist: {data_dir}")

if __name__ == "__main__":
    check_environment() 