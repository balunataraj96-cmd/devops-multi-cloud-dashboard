import os
import boto3
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environmental variables
load_dotenv(dotenv_path="../config/.env")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

app = Flask(__name__)
CORS(app) # Allows Grafana to talk to this script securely

@app.route('/api/aws/stop-all', methods=['POST'])
def stop_all_ec2():
    print("[!] EMERGENCY KILL SWITCH ACTIVATED VIA DASHBOARD!")
    ec2_client = boto3.client('ec2', region_name=REGION)
    
    try:
        # 1. Find all running EC2 instances
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        instance_ids = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_ids.append(instance['InstanceId'])
        
        # 2. If no instances are running, return safely
        if not instance_ids:
            return jsonify({"status": "success", "message": "No running resources detected. Budget is safe!"}), 200
            
        # 3. Stop the running instances
        print(f"[*] Stopping target instances: {instance_ids}")
        ec2_client.stop_instances(InstanceIds=instance_ids)
        
        return jsonify({
            "status": "success", 
            "message": f"Successfully stopped {len(instance_ids)} active nodes!",
            "terminated_assets": instance_ids
        }), 200
        
    except Exception as e:
        print(f"[!] Kill switch failure: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the web control server on local port 5000
    print("=== DEVOPS DASHBOARD CONTROL ENGINE ACTIVE ON PORT 5000 ===")
    app.run(host='0.0.0.0', port=5000)
