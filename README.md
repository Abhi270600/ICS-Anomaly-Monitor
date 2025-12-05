# 🛡️ Real-Time OT Anomaly Detection System

A Python-based simulation of an Industrial Control System (ICS) designed to detect **Insider Threats** using Unsupervised Machine Learning. This project creates a "Digital Twin" of an industrial pumping station to spot process anomalies (e.g., pressure spikes) and behavioral threats (e.g., off-hours access) in real-time.

---

## 📖 Overview

Operational Technology (OT) networks are vulnerable to insider threats—attacks that look "technically valid" to firewalls (e.g., an authorized user sending a command) but are malicious in context.

This project implements an **Anomaly Detection System (ADS)** using the **Isolation Forest** algorithm. It monitors a simulated SCADA network bus and correlates physical telemetry (Physics) with user metadata (Behavior) to flag malicious activity without relying on known attack signatures.

### Key Features
* **Digital Twin Simulation:** Simulates realistic pump physics (Sine wave pressure cycles) and thermal dynamics.
* **Unsupervised Learning:** Uses `sklearn.IsolationForest` to detect unknown zero-day attacks.
* **Multi-Variate Analysis:** Correlates 4 distinct features: `Pressure`, `Temperature`, `ICS Write Frequency`, and `Login Hour`.
* **Live Attack Injection:** Includes an interactive tool to launch 5 distinct insider attack scenarios.

---

## 🏗️ Architecture

The system follows a modular architecture mimicking a real-world OT environment:

```mermaid
flowchart LR
    %% Define Styles
    classDef legitimate fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef attacker fill:#ffebee,stroke:#b71c1c,stroke-width:2px,stroke-dasharray: 5 5;
    classDef security fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef storage fill:#fff3e0,stroke:#e65100,stroke-width:2px,shape:cyl;

    subgraph OT_Environment ["Operational Technology Layer"]
        direction TB
        PLC[("💻 PLC / Sensors<br/>(sensor_simulator.py)")]:::legitimate
        Actuators("⚙️ Pumps & Valves"):::legitimate
        Physics("📈 Process Physics<br/>(Sine Wave Logic)"):::legitimate
        
        Physics --> PLC
        PLC -- "Normal Telemetry<br/>(Pressure/Temp)" --> Actuators
    end

    subgraph Threat_Actor ["Attack Surface"]
        Insider("🕵️ Insider Threat<br/>(attacker.py)"):::attacker
        Toolkit("💉 Injection Tool"):::attacker
        
        Insider --> Toolkit
    end

    subgraph Network ["SCADA Network Bus"]
        DataBus[("📄 Shared Data Bus<br/>(shared_data.csv)")]:::storage
    end

    subgraph Security_SOC ["Security Operations Center"]
        Monitor("🛡️ Anomaly Detector<br/>(monitor.py)"):::security
        ML_Model("🧠 Isolation Forest<br/>(Machine Learning)"):::security
        Dashboard("📊 Operator HMI<br/>(plot_results.py)"):::security
        
        Monitor <--> ML_Model
        Monitor --> |"🚨 Alert Triggered"| Dashboard
    end

    %% Connections
    PLC --> |"Write (0.5s)"| DataBus
    Toolkit --> |"False Data Injection"| DataBus
    DataBus --> |"Poll (0.2s)"| Monitor

    %% Annotations
    linkStyle 4 stroke:#b71c1c,stroke-width:3px;

---

## 📂 Project Structure

### sensor_simulator.py — *The Plant*  
Generates “normal” Modbus-like telemetry:
- Pressure ≈ 55 PSI (Gaussian noise)
- Temperature ≈ 110°F (Gaussian noise)

This acts as the baseline physical process.

### monitor.py — *The Defense*  
A polling-based monitoring engine that:
- Trains an ML model on baseline sensor data  
- Monitors real-time telemetry  
- Flags physical, cyber, or behavioral anomalies  

### attacker.py — *The Threat*  
Interactive attack console.  
Simulates multiple OT attack vectors:
- Physics manipulation  
- Network floods  
- Behavioral anomalies  
- Coordinated multi-stage attacks  

### plot_results.py — *The HMI*  
Generates a 3‑panel dashboard showing:
- Physical process evolution  
- Anomaly detection events  
- Cyber activity timeline  

### shared_data.csv — *The Network*  
Shared communication bus (file-based historian).  
All components read/write from/to this file.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies
```bash
pip install pandas scikit-learn matplotlib

