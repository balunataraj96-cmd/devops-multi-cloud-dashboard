import os
import datetime
import json
import boto3
import psycopg2
from dotenv import load_dotenv

# 1. Load system environmental configurations safely
load_dotenv(dotenv_path="../config/.env")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Database connectivity properties
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "devops_metrics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_aws_cost_data():
    """Fetches current month-to-date blended costs via AWS Cost Explorer API."""
    print("[*] Contacting AWS Cost Explorer endpoint...")
    client = boto3.client('ce', region_name=REGION)
    
    today = datetime.date.today()
    start_date = today.replace(day=1).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    if start_date == end_date:
        start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    
    try:
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['BlendedCost']
        )
        
        # FIX: 'ResultsByTime' is a list. We must extract the first item [0]
        # and then access the nested Total -> BlendedCost metric maps.
        results_list = response.get('ResultsByTime', [])
        if not results_list:
            print("[!] Empty result list returned from AWS Cost Explorer.")
            return None
            
        cost_record = results_list[0]['Total']['BlendedCost']
        return {
            "amount": float(cost_record['Amount']),
            "currency": cost_record['Unit']
        }
    except Exception as e:
        print(f"[!] Error fetching AWS billing metrics: {e}")
        return None


def get_aws_resource_inventory():
    """Counts active running infrastructure processing compute instances."""
    print("[*] Scanning active EC2 instance infrastructure inventory...")
    ec2_client = boto3.client('ec2', region_name=REGION)
    try:
        response = ec2_client.describe_instances()
        running_instances = 0
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                if instance['State']['Name'] == 'running':
                    running_instances += 1
        return {"active_nodes": running_instances}
    except Exception as e:
        print(f"[!] Error scanning EC2 footprints: {e}")
        return None

def save_metrics_to_db(cost_info, inventory_info):
    """Establishes database transaction boundaries and commits metrics securely."""
    if not cost_info or not inventory_info:
        print("[!] Incomplete operational data. Aborting database save operation.")
        return
        
    print(f"[*] Opening transaction handshake with database '{DB_NAME}'...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO cloud_metrics (provider, metric_type, amount, currency, active_nodes)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        # Structure payload values to align directly with schema expectations
        data_tuple = (
            "AWS",
            "UnifiedMetrics",
            cost_info["amount"],
            cost_info["currency"],
            inventory_info["active_nodes"]
        )
        
        cursor.execute(insert_query, data_tuple)
        conn.commit()
        print("[+] SUCCESS: Data securely written to local PostgreSQL database table!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[!] Critical database transaction failure: {e}")

if __name__ == "__main__":
    print("=== RUNNING INTEGRATED DEVOPS EXTRACTION PIPELINE ===")
    
    # 1. Fetch live metrics from AWS
    billing_data = get_aws_cost_data()
    inventory_data = get_aws_resource_inventory()
    
    # 2. Write those metrics directly into our storage table
    save_metrics_to_db(billing_data, inventory_data)
