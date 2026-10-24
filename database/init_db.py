import os
import psycopg2
from dotenv import load_dotenv

# Load database configuration details safely
load_dotenv(dotenv_path="../config/.env")

# Fallback credentials for local developer environment setup
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "devops_metrics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "CHANGE_TO_YOUR_POSTGRES_PASSWORD") # Put your real password here!
DB_PORT = os.getenv("DB_PORT", "5432")

def initialize_database():
    print("[*] Establishing administrative connection to PostgreSQL engine...")
    
    # Connect to the default system database first to create our project database safely
    conn = psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT, database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create a fresh database for our project if it doesn't exist
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"[+] Database '{DB_NAME}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"[*] Database '{DB_NAME}' already exists. Moving forward...")
        
    cursor.close()
    conn.close()

    # Now, connect directly to our new devops_metrics database to build the tables
    print(f"[*] Connecting to database '{DB_NAME}' to configure schemas...")
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cursor = conn.cursor()
    
    # Define our core metrics table layout
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cloud_metrics (
        id SERIAL PRIMARY KEY,
        provider VARCHAR(50) NOT NULL,
        metric_type VARCHAR(50) NOT NULL,
        amount NUMERIC(12, 4),
        currency VARCHAR(10),
        active_nodes INT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    print("[+] Table structure 'cloud_metrics' initialized successfully!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("=== INITIALIZING DEVOPS DATABASE ENGINE ===")
    initialize_database()
