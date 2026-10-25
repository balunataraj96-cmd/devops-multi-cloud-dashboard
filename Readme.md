# Multi-Cloud DevOps Resource and Cost Governance Dashboard

An enterprise-grade, budget-conscious telemetry dashboard pipeline designed to aggregate, parse, persist, and visualize infrastructure usage and cost metrics across a multi-cloud topography. The architecture is explicitly designed to handle programmatic cloud data stream collections, multi-engine relational storage routing, and automated closed-loop remediation mitigation workflows.

---
## Phase 1 Deliverable: Amazon AWS Cloud Integration
## 📊 Systems Topology & Telemetry Architecture Diagram

The monitoring network architecture organizes workloads into decoupled processing layers. The structural layout traces telemetry processing events from initial cloud API ingestion points down through local transactional database persistence frameworks, alongside synchronous webhook incident control tracks.

```text
+-------------------------------------------------------------------------------------------------------------------------------+

|                                            MULTICLOUD INFRASTRUCTURE RESOURCE LAYER                                           |
|                                                                                                                               |
|   +--------------------------+          +---------------------------+          +--------------------------+                   |
|   |  AMAZON WEB SERVICES     |          |   MICROSOFT AZURE (*)     |          |  GOOGLE CLOUD PLATFORM(*)|                   |
|   |  ====================    |          |   ===================     |          |  ======================= |                   |
|   |  * Cost Explorer API     |          |   * Consumption API       |          |  * Cloud Billing API     |                   |
|   |  * EC2 Fleet Discovery   |          |   * Compute Virtual Mach. |          |  * Compute Engine Engine |                   |
|   +--------------------------+          +---------------------------+          +--------------------------+                   |
+-------------------------------------------------------------------------------------------------------------------------------+

              |                                                 |                                      |
              | 1. Ingest Inbound Telemetry Payload Streams     | (* Planned Expansion Sprints)        |
              v                                                 v                                      v
+-------------------------------------------------------------------------------------------------------------------------------+

|                                            DATA STREAM INGESTION & PIPELINE LAYER                                             |
|                                                                                                                               |
|   +-----------------------------------------------------------------------------------------------------------------------+   |
|   |  INGESTION DISCOVERY CORE (App: backend/aws_aggregator.py)                                                            |   |
|   |  ========================================================                                                             |   |
|   |  * Runtime Engine Context: Python 3.x Script Execution Daemon                                                         |   |
|   |  * Internal Module Libraries: Ingests Boto3 SDK Core APIs / Parses Structural Multi-Nested JSON Payload Blocks        |   |
|   +-----------------------------------------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------------------------------------+
              |                                                                                        ^

              | 2. Reformat to Standard Flat Dict Structure                                            | 5. Dispatch Sync POST
              v                                                                                        |    Emergency API Kill
+--------------------------------------------------------------------------------------------------+   |    Command String

|                                     LOCAL SYSTEM STORAGE & REPOSITORY INTERFACE LAYER            |   |
|                                                                                                  |   |
|   +---------------------------------------+              +-----------------------------------+   |   |
|   | PERSISTENT TRANSACTIONAL DATA ENGINE  |              | AUTOMATED RESPONSE GATEWAY INTERF.|   |   |
|   | ====================================  |              | ================================= |   |   |
|   | * Engine Type: PostgreSQL Relational  |              | * Middleware App: backend/app.py  |   |   |
|   | * Database Allocation: devops_metrics |              | * Micro-Framework: Python Flask   |   |   |
|   | * Operational Port Mapping: 5432      |              | * Security Protocol: Flask-CORS   |   |   |
|   | * Dynamic Schema Table: cloud_metrics |              | * Operational Port Mapping: 5000  |   |   |
|   +---------------------------------------+              +-----------------------------------+   |   |
+--------------------------------------------------------------------------------------------------+   |

              |                                                                                        |
              | 3. Continuous Active SQL Read Polling                                                  | 4. Issue Asynchronous
              v                                                                                        |    Webhook Control Trigger
+--------------------------------------------------------------------------------------------------+   |

|                                    ANALYTICS INTERFACE & METRICS PRESENTATION LAYER              |   |
|                                                                                                  |   |
|   +------------------------------------------------------------------------------------------+   |   |
|   | PERFORMANCE ANALYTICS UI WORKSPACE (Engine: Grafana OSS | Local Network Port: 3000)       |   |   |
|   | ======================================================================================== |   |   |
|   | * Panel View 1: Real-Time Live Monthly MTD Budget Expenditure Tracker (Stat Model UI)    | --+   |
|   | * Panel View 2: Chronological Active Compute Cluster Infrastructure Node Graph Tracker   |       |
|   | * Control Center Panel: HTML Action Interface Configuration (Interactive JS Trigger Box)  |       |
|   +------------------------------------------------------------------------------------------+       |
+------------------------------------------------------------------------------------------------------+

=================================================================================================================================
     DATA VECTOR PATHWAYS:  === Telemetry Ingestion Ingress Pipeline ===> ===> ===> ===>
     REMEDIATION PATHWAYS:  === Emergency Automated Incident Control Switch ===> ===> ===>
=================================================================================================================================
```

---

## 🛠 Complete Architectural Implementation Blueprint

### 1. Security Architecture & IAM Least-Privilege Access Configuration
To safeguard organizational cloud balances, access keys belonging to the global AWS Root account were explicitly restricted. A programmatic service user was constructed within the Identity and Access Management (IAM) module to act as the primary authentication bridge.
* **IAM Entity Identification:** `dashboard-aggregator`
* **Credential Profile Topology:** Secure programmatic access key-pair configurations managed locally via the standard AWS Command Line Interface (CLI).
* **Policy Architecture Matrix:**
  * `AWSBillingReadOnlyAccess`: Restricts programmatic access limits to read-only consumption of the AWS Cost Explorer API metrics engine.
  * `AmazonEC2ReadOnlyAccess`: Grants structured visibility to pull deployment parameters from the elastic compute inventory dashboard.
  * `AmazonS3ReadOnlyAccess`: Provides simple data-index parsing routines across object storage components while preventing any resource modifications.

---

### 2. Live API Communication Verification
Before writing the core software automation layers, direct network handshakes with the AWS global telemetry endpoints were verified using the terminal command-line framework. 
```bash
aws ce get-cost-and-usage --time-period Start=2026-10-01,End=2026-10-24 --granularity MONTHLY --metrics "BlendedCost"
```
The endpoint successfully completed cryptographic verification, returning an active JSON billing payload tracking the monthly cost threshold down to exact float values.

#### 📍 Visual Reference Point 1
 
> ![AWS CLI API Connection Verification](./assets/01_aws_cli_test.png)

---

### 3. Isolated Development Environment Structuring
The repository workspace was separated into structural sub-directories to cleanly decouple operational layers, preparing the codebase to easily accept alternate cloud vendors (Azure/GCP) in later sprints:
* `/backend`: Holds data collection automation logic, API handlers, and the closed-loop remediation microservice application scripts.
* `/database`: Allocated for local transactional storage configuration and relational mapping schemas.
* `/config`: Dedicated to runtime environments, shielding credentials out of the codebase using a custom `.env` profile layer.

```text
devops-cost-dashboard/
├── assets/
│   ├── 01_aws_cli_test.png
│   ├── 02_python_aggregator_output.png
│   ├── 03_database_initialization.png
│   ├── 04_integrated_pipeline_success.png
│   ├── 05_grafana_query_editor.png
│   ├── 06_grafana_main_dashboard.png
│   └── 07_emergency_kill_switch.png
├── backend/
│   ├── app.py
│   └── aws_aggregator.py
├── config/
│   └── .env (Git-ignored)
├── database/
│   └── init_db.py
└── .gitignore
```

---

### 4. Modular Python Ingestion Engine Development
A background collection daemon was built inside the `/backend` folder using the Python standard library wrapped around the official `boto3` SDK layer. 
* **Dynamic Time Windows:** Uses internal mathematical calendar boundaries via Python `datetime` objects to calculate month-to-date run windows, completely eliminating static hard-coded time strings.
* **Raw Payload Normalization:** Intercepts massive multi-nested JSON payloads from cloud API arrays, strips out redundant information, and maps the metrics into flat dictionary formats.

```bash
python aws_aggregator.py
```

#### 📍 Visual Reference Point 2

> ![Python Data Extractor Operational Output](./assets/02_python_aggregator_output.png)

---

### 5. Persistent Storage Layer Implementation (PostgreSQL)
To run the platform at zero operational cost, a relational database stack was deployed locally instead of using an active AWS RDS cloud instance.
* **Driver Architecture:** Uses the `psycopg2-binary` abstraction layer to connect Python processing threads to the transactional database engine.
* **Chronological Data Tracing Schema:** Configured table keys to log real-time metadata metrics along an automated timestamp trajectory (`recorded_at`).

```bash
py init_db.py
```

#### 📍 Visual Reference Point 3

> ![Local PostgreSQL Table Schema Generation](./assets/03_database_initialization.png)

---

### 6. Pipeline Integration & Transactional Ingestion Testing
The data collection component and storage layer scripts were fused together into a unified transactional engine (`backend/aws_aggregator.py`). When executed, this integrated module calls AWS APIs, reformats the JSON content, opens a secure transactional channel to the local database container, and commits a persistent record into the data table.

```bash
py aws_aggregator.py
```

#### 📍 Visual Reference Point 4

> ![Integrated Telemetry Ingestion Output](./assets/04_integrated_pipeline_success.png)

---

### 7. Analytical Dashboard Customization (Grafana)
Grafana OSS was installed locally to serve as the main web interface dashboard, connecting to our database via standard loopback channels on port `5432`.
* **Data Source Connectivity:** Verified using structural TCP/IP database authentication handshakes with custom SSL protection markers explicitly set to `disabled`.
* **Telemetry Queries:** Relational SQL string routines were written within Grafana's query code editor window to dynamically extract target data rows:

```sql
/* Live Financial Meter Query */
SELECT amount FROM cloud_metrics WHERE provider = 'AWS' ORDER BY recorded_at DESC LIMIT 1;

/* Historic Computing Fleet Node Timeline Graph Query */
SELECT recorded_at AS time, active_nodes FROM cloud_metrics WHERE provider = 'AWS' ORDER BY recorded_at ASC;
```

#### 📍 Visual Reference Point 5

> ![Grafana SQL Code Interface Configuration](./assets/05_grafana_query_editor.png)

#### 📍 Visual Reference Point 6

> ![Live Multi-Cloud Operational Management UI](./assets/06_grafana_main_dashboard.png)

---

### 8. Closed-Loop Incident Remediation Engine (Active Governance Kill-Switch)
To change the dashboard from a passive readout into an active cost governance command center, an asynchronous automation microservice was introduced.
* **IAM Privilege Elevation:** Upgraded the programmatic service account role permissions to include `AmazonEC2FullAccess` capabilities.
* **REST API Middleware:** Built a lightweight local web service using `Flask` and `Flask-CORS` (`backend/app.py`), listening for calls on port `5000`.
* **Web Button Front-End:** Embedded an interactive HTML button with automated JavaScript handling directly within the Grafana workspace layout. Clicking the button shoots an asynchronous `POST` web request back to the Flask server, triggering a live target sweep that instantly stops all active billing servers in AWS.

#### 📍 Visual Reference Point 7

> ![Interactive Remediation Action Button Panel](./assets/07_emergency_kill_switch.png)

---
## Phase 2 Deliverable: Microsoft Azure Cloud Integration

### 1. Abstract & Azure IAM Entitlements Configuration
Phase 2 maps the expansion of the multi-cloud dashboard telemetry pipeline into the Microsoft Azure public cloud ecosystem. To ensure unified tracking patterns and adhere to strict budget parameters, credential authorizations were configured using Azure Active Directory App Registrations to establish a dedicated Service Principal identity (`azure-dashboard-aggregator`).

* **Role Definition Assignment:** The Service Principal entity was assigned a specialized security scope mapped directly to the **`Reader`** role within the active subscription directory framework. This limits script permissions to descriptive discovery parameters and cost allocations, blocking any ability to spin up billable assets.
* **Cryptographic Vault Injection:** Authentication handshakes are authorized dynamically using isolated environmental profiles (`.env`), binding Client IDs, Tenant IDs, and Client Secrets securely outside code execution arrays.

### 2. Relational Multi-Cloud Ingestion Schema
Telemetry data collected from Azure Python pipelines is mapped directly into our central relational table, utilizing targeted data types to ensure consistent parsing behavior:

```sql
/* Query mapping current Azure infrastructure footprints */
SELECT recorded_at AS time, active_nodes FROM cloud_metrics WHERE provider = 'AZURE' ORDER BY recorded_at ASC;
```

### 3. Feature Branch Version Isolation Management
To maintain sound code tracking practices, all Azure development scripts were managed inside an isolated Git tracking workspace before deployment to primary release versions:
* **Branch Isolation Tracking ID:** `feature/azure-base`
* **Commit Ingestion Hash Profile:** `feat: integrate azure metrics extraction engine and postgres persistence`


## ⚠️ Core Engineering Roadblocks & Strategic Resolution Matrix

### 🪵 1. Deprecated Policy Specifications in IAM Directories
* **The Hurdle:** Historical DevOps study blueprints recommended attaching a specific AWS monitoring policy (`AWSInsightsReadOnlyAccess`). During live deployment, the AWS IAM search index failed to find this exact string, blocking credential setup.
* **The Resolution:** Successfully transitioned to modern cloud-native policy definitions, attaching a precise combination of `AWSBillingReadOnlyAccess`, `AmazonEC2ReadOnlyAccess`, and `AmazonS3ReadOnlyAccess` to enforce least-privilege security.


### 🪵 2. Windows Environment Variable Path Conflicts

* **The Hurdle:** Running the database schema file with standard terminal commands failed, throwing a shell environment redirection error that forced open the Microsoft Windows App Store.
* **The Resolution:** Fixed by entering the advanced Windows system preferences panel to toggle off App Execution Aliases for Python executables, then modifying terminal execution statements to run through the explicit py utility engine wrapper.

### 🪵 3. Multi-Nested JSON Array Extraction Failure

* **The Hurdle:** When testing the integrated database script, the program crashed with a critical dictionary error (TypeError: list indices must be integers or slices, not str).
* **he Resolution:** Investigated the AWS Cost Explorer API output schema and realized ResultsByTime is delivered as a structured list array. Patched the code's index logic to target the active list index (results_list['Total']['BlendedCost']) before executing structural payload dumps.

### 🪵 4. Cross-Origin Resource Sharing (CORS) Security Interrupts

* **The Hurdle:** The front-end dashboard engine initially failed to trigger instance shutdowns because web browsers block raw requests going between different local ports (Port 3000 to Port 5000).
* **The Resolution:** Ingested the flask-cors helper library into the backend runtime environment, wrapping the application context object (CORS(app)) to pass structural cross-origin validation headers cleanly.

### 🪵 5. Grafana HTML/XSS Script Stripping

* **The Hurdle:** The front-end remediation panel leaked raw text strings across the interface layout because Grafana's safety filters standard scrub out active <script> components to prevent cross-site scripting vulnerabilities.
* **he Resolution:** Bypassed this layout defect by opening the core system configuration file (C:\Program Files\GrafanaLabs\grafana\conf\defaults.ini), setting the security option disable_sanitize_html = true, and restarting the background Windows architecture service.