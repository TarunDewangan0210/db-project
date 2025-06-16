import os
import pandas as pd
import json
from datetime import datetime

def validate_csv_file(file_path, required_columns=None):
    """Validate a CSV file and return its structure"""
    try:
        df = pd.read_csv(file_path)
        print(f"\nValidating {os.path.basename(file_path)}:")
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print("Columns and their data types:")
        
        # Analyze each column
        column_info = {}
        for column in df.columns:
            # Get sample values
            sample_values = df[column].dropna().head(3).tolist()
            # Determine data type
            dtype = str(df[column].dtype)
            # Check for null values
            null_count = df[column].isnull().sum()
            
            column_info[column] = {
                'dtype': dtype,
                'sample_values': sample_values,
                'null_count': null_count,
                'unique_count': df[column].nunique()
            }
            
            print(f"\n{column}:")
            print(f"  - Data type: {dtype}")
            print(f"  - Sample values: {sample_values}")
            print(f"  - Null values: {null_count}")
            print(f"  - Unique values: {df[column].nunique()}")
        
        # Validate required columns if specified
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"\nWARNING: Missing required columns: {missing_columns}")
                return False, column_info
        
        return True, column_info
    
    except Exception as e:
        print(f"Error validating {file_path}: {str(e)}")
        return False, None

def generate_sql_schema(column_info, table_name):
    """Generate SQL schema based on column information"""
    sql_types = {
        'int64': 'INTEGER',
        'float64': 'DECIMAL(10,2)',
        'object': 'VARCHAR(255)',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }
    
    columns = []
    for col_name, info in column_info.items():
        # Determine SQL type
        dtype = info['dtype']
        if 'int' in dtype:
            sql_type = 'INTEGER'
        elif 'float' in dtype:
            sql_type = 'DECIMAL(10,2)'
        elif 'datetime' in dtype:
            sql_type = 'TIMESTAMP'
        elif 'bool' in dtype:
            sql_type = 'BOOLEAN'
        else:
            # For string types, determine appropriate length
            max_length = max(len(str(val)) for val in info['sample_values']) if info['sample_values'] else 255
            sql_type = f'VARCHAR({max(50, min(max_length * 2, 1000))})'
        
        # Add NOT NULL constraint if no null values
        not_null = 'NOT NULL' if info['null_count'] == 0 else ''
        
        columns.append(f"    {col_name} {sql_type} {not_null}")
    
    # Generate CREATE TABLE statement
    create_table = f""" CREATE TABLE {table_name} (
      {',\n'.join(columns)}
    ); """
    
    return create_table

def main():
    # Define the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eep-db-storage")
    
    # Define required columns for each table
    required_columns = {
        'customers.csv': ['customer_id', 'name', 'email', 'address'],
        'products.csv': ['product_id', 'name', 'price'],
        'orders.csv': ['order_id', 'customer_id', 'order_date', 'total_amount'],
        'orderdtl.csv': ['order_id', 'product_id', 'quantity', 'unit_price']
    }
    
    # Validate each CSV file and generate schemas
    schemas = {}
    for file_name, required_cols in required_columns.items():
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            print(f"\n{'='*50}")
            print(f"Processing {file_name}")
            print(f"{'='*50}")
            
            is_valid, column_info = validate_csv_file(file_path, required_cols)
            if is_valid and column_info:
                table_name = file_name.replace('.csv', '')
                schema = generate_sql_schema(column_info, table_name)
                schemas[table_name] = schema
                
                print(f"\nGenerated schema for {table_name}:")
                print(schema)
            else:
                print(f"\nSkipping schema generation for {file_name} due to validation errors")
        else:
            print(f"\nFile not found: {file_path}")
    
    # Save schemas to a file
    if schemas:
        schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_schemas.sql")
        with open(schema_file, 'w') as f:
            f.write("-- Generated SQL Schemas\n")
            f.write("-- Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            for table_name, schema in schemas.items():
                f.write(f"-- Schema for {table_name}\n")
                f.write(schema)
                f.write("\n\n")
        
        print(f"\nSchemas have been saved to: {schema_file}")

if __name__ == "__main__":
    main() 