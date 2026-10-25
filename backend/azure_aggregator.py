import os
import datetime
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.consumption import ConsumptionManagementClient

# 1. Load configuration and environment parameters safely
load_dotenv(dotenv_path="../config/.env")

# Map environment variables into the script context
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

# Set credentials implicitly for the Azure identity manager
os.environ["AZURE_TENANT_ID"] = TENANT_ID if TENANT_ID else ""
os.environ["AZURE_CLIENT_ID"] = CLIENT_ID if CLIENT_ID else ""
os.environ["AZURE_CLIENT_SECRET"] = CLIENT_SECRET if CLIENT_SECRET else ""

def get_azure_resource_inventory():
    """
    Connects to Azure Resource Manager API and queries the total count
    of active virtual machines across the subscription.
    """
    print("[*] Initializing Azure Resource Manager connection client...")
    try:
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
        
        # List all computing infrastructure resources across the subscription scope
        resources = resource_client.resources.list(filter="resourceType eq 'Microsoft.Compute/virtualMachines'")
        
        vm_count = 0
        for vm in resources:
            vm_count += 1
            
        return {
            "provider": "AZURE",
            "metric_type": "ResourceInventory",
            "active_nodes": vm_count
        }
    except Exception as e:
        print(f"[!] Error tracking Azure resource footprints: {e}")
        return {"provider": "AZURE", "metric_type": "ResourceInventory", "active_nodes": 0}

def get_azure_cost_data():
    """
    Queries the Azure Consumption API to extract month-to-date metric expenditures,
    handling modern billing contract models securely.
    """
    print("[*] Contacting Azure Consumption billing endpoint...")
    try:
        credential = DefaultAzureCredential()
        consumption_client = ConsumptionManagementClient(credential, f"/subscriptions/{SUBSCRIPTION_ID}")
        
        today = datetime.date.today()
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        
        if start_date == end_date:
            start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            
        scope = f"subscriptions/{SUBSCRIPTION_ID}"
        print(f"[*] Querying Azure billing metrics from {start_date} to {end_date}...")
        
        usage_details = consumption_client.usage_details.list(
            scope=scope,
            filter=f"properties/usageStart ge '{start_date}' and properties/usageEnd le '{end_date}'"
        )
        
        total_cost = 0.0
        currency = "USD"
        
        for item in usage_details:
            # Modern usage accounts wrap metric costs under item.cost_in_billing_currency
            # Older profiles map metrics under item.pretax_cost
            cost_value = getattr(item, 'cost_in_billing_currency', getattr(item, 'pretax_cost', 0.0))
            total_cost += float(cost_value or 0.0)
            
            if hasattr(item, 'billing_currency') and item.billing_currency:
                currency = item.billing_currency
            elif hasattr(item, 'currency') and item.currency:
                currency = item.currency
                
        return {
            "provider": "AZURE",
            "metric_type": "Cost",
            "amount": round(total_cost, 4),
            "currency": currency
        }
    except Exception as e:
        print(f"[!] Azure Consumption API error, deploying fallback defaults: {e}")
        return {
            "provider": "AZURE",
            "metric_type": "Cost",
            "amount": 0.0000,
            "currency": "USD"
        }

import psycopg2

# Database connectivity properties mapped from the single central .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "devops_metrics")
DB_USER = os.getenv("DB_USER", "postgres")
# Using the exact same password string we built for the AWS module
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")

def save_azure_metrics_to_db(resource_info, cost_info):
    """Establishes database transaction boundaries and commits Azure metrics securely."""
    print(f"[*] Opening transaction handshake with database '{DB_NAME}' for Azure ingestion...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO cloud_metrics (provider, metric_type, amount, currency, active_nodes)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        # Structure values to write a clean database row entry labeled as 'AZURE'
        data_tuple = (
            "AZURE",
            "UnifiedMetrics",
            cost_info["amount"],
            cost_info["currency"],
            resource_info["active_nodes"]
        )
        
        cursor.execute(insert_query, data_tuple)
        conn.commit()
        print("[+] SUCCESS: Azure telemetry securely committed to local PostgreSQL database!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[!] Critical database transaction failure for Azure stream: {e}")

if __name__ == "__main__":
    print("=== RUNNING INTEGRATED AZURE EXTRACTION PIPELINE ===")
    
    # 1. Fetch live telemetry metrics from Microsoft Azure APIs
    azure_resources = get_azure_resource_inventory()
    azure_costs = get_azure_cost_data()
    
    # 2. Persist the metrics inside our unified transactional database
    save_azure_metrics_to_db(azure_resources, azure_costs)

