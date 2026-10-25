import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

load_dotenv(dotenv_path="../config/.env")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

# Bind Azure environment variables explicitly for SDK authentication
os.environ["AZURE_TENANT_ID"] = os.getenv("AZURE_TENANT_ID", "")
os.environ["AZURE_CLIENT_ID"] = os.getenv("AZURE_CLIENT_ID", "")
os.environ["AZURE_CLIENT_SECRET"] = os.getenv("AZURE_CLIENT_SECRET", "")

app = Flask(__name__)
CORS(app)

@app.route('/api/aws/stop-all', methods=['POST'])
def stop_all_ec2():
    print("[!] EMERGENCY AWS KILL SWITCH ACTIVATED VIA DASHBOARD!")
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    try:
        response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        instance_ids = [inst['InstanceId'] for res in response.get('Reservations', []) for inst in res.get('Instances', [])]
        if not instance_ids:
            return jsonify({"status": "success", "message": "No running AWS resources detected. Budget safe!"}), 200
        ec2_client.stop_instances(InstanceIds=instance_ids)
        return jsonify({"status": "success", "message": f"Successfully stopped {len(instance_ids)} active AWS nodes!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/azure/stop-all', methods=['POST'])
def stop_all_azure_vms():
    print("[!] EMERGENCY AZURE KILL SWITCH ACTIVATED VIA DASHBOARD!")
    try:
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, AZURE_SUBSCRIPTION_ID)
        
        # 1. Discover all virtual machines across the subscription scope
        vm_list = compute_client.virtual_machines.list_all()
        stopped_vms = []
        
        for vm in vm_list:
            # Extract Resource Group name safely out of the long Azure resource ID string
            resource_group = vm.id.split("/resourceGroups/")[1].split("/")[0]
            
            print(f"[*] Dispatching PowerOff command string to Azure VM: {vm.name} inside RG: {resource_group}...")
            # 2. Issue the immediate deallocate execution tracking call (Stops billing completely)
            compute_client.virtual_machines.begin_deallocate(resource_group, vm.name)
            stopped_vms.append(vm.name)
            
        if not stopped_vms:
            return jsonify({"status": "success", "message": "No running Azure resources detected. Budget safe!"}), 200
            
        return jsonify({"status": "success", "message": f"Successfully deallocated {len(stopped_vms)} active Azure VMs!"}), 200
    except Exception as e:
        print(f"[!] Azure Kill switch failure: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("=== DEVOPS DASHBOARD MULTI-CLOUD CONTROL ENGINE ACTIVE ON PORT 5000 ===")
    app.run(host='0.0.0.0', port=5000)
