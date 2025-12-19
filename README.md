# FlowSight: Real-Time Traffic Congestion Forecasting Pipeline

FlowSight is a real-time traffic analytics and forecasting pipeline designed as a Big Data course project (ICS-474).
It simulates live traffic sensor data, processes it using Kafka and Spark Structured Streaming, stores it in a Parquet data lake and PostgreSQL, trains a machine learning model, and exposes insights through an API and interactive dashboard.

The project demonstrates an end-to-end data engineering pipeline, covering ingestion, stream processing, storage, analytics, and visualization.

(Built on this peoject "https://github.com/khush-i97/FlowSight"

## ✨ Project Highlights

- Real-time traffic data simulation using Kafka
- Stream processing with PySpark Structured Streaming or pure‑Python consumer
- Parquet-based data lake (bronze layer)
- PostgreSQL for persistent structured storage
- Traffic speed prediction with a Random Forest model
- REST API for live predictions via FastAPI
- Interactive Streamlit dashboard with map visualization

---

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.10+
- Java 17 (Temurin or Oracle JDK)
- Apache Spark 3.4+ (used via PySpark in WSL2)
- Docker Desktop (Kafka, Zookeeper, PostgreSQL)
- WSL2 (Ubuntu) – required for Spark on Windows
- Git

### Clone the Repository

```bash
git clone https://github.com/FMoutaz/BigData-FlowSight.git
cd BigData-FlowSight/FlowSight-upstream
```

Create and Activate Virtual Environments
Windows (Producer, API, Dashboard)
py -m venv venv
venv\Scripts\activate

WSL (Spark Streaming)
python3 -m venv venv_wsl
source venv_wsl/bin/activate

Install Python Dependencies
pip install -r requirements.txt


Virtual environments, generated data, and checkpoints are excluded from version control.

🚗 Pipeline Execution
1. Start Kafka & Zookeeper (Docker)
docker compose -f docker-compose.yaml up -d
docker ps


Kafka runs on localhost:9092
Zookeeper runs on localhost:2181

2. Start PostgreSQL (Docker)
docker compose -f docker-compose.storage.yaml up -d
docker ps


PostgreSQL runs on localhost:5432.

3. Simulate Traffic Data
python producer.py


This continuously generates synthetic traffic sensor events and publishes them to the Kafka topic traffic.

4. Stream to Bronze Layer (Spark Structured Streaming – WSL)
python stream_to_parquet.py


Consumes Kafka topic traffic

Writes streaming data to data/bronze/

Uses checkpointing in checkpoint/bronze/

Runs continuously in real time

5. Train the Machine Learning Model
python train_model.py


This trains a RandomForest Regressor on historical streaming data stored in Parquet.

Training Summary

Parquet files used: 196

Training samples: 380

Testing samples: 95

Mean Absolute Error (MAE): 15.84

The trained model is saved as:

model.joblib

6. Launch the FastAPI Service
python -m uvicorn app:app --reload


Open API documentation at:

http://127.0.0.1:8000/docs

📊 Sample /predict Usage

Request

{
  "sensor": "roadA",
  "speed": 48.3,
  "timestamp": 1627810200
}


Response

{
  "predicted_speed_next": 50.1
}

7. Run the Streamlit Dashboard
streamlit run dashboard.py


Access the dashboard at:

http://localhost:8501


The dashboard visualizes real-time and historical traffic trends.

8. Verify PostgreSQL Storage (Optional)
docker exec -it flowsight-upstream-postgres-1 \
psql -U flowsight -d flowsight_db \
-c "SELECT * FROM traffic_events LIMIT 5;"

## 🌐 Interactive Dashboard

You can start the dashboard UI as follows:

```powershell
# If the streamlit.exe launcher stub is broken, bypass it with:
python -m streamlit run dashboard.py
# Or if your stub is working, simply run:
streamlit run dashboard.py
```

This will open the dashboard at <http://localhost:8501>. Use the sidebar to pick a sensor, enter speed, and view predicted congestion on a map.
<img width="1895" height="842" alt="image" src="https://github.com/user-attachments/assets/4678c6b3-614b-4b76-b266-740d9b467659" />



---

## 🌟 Conclusion

FlowSight integrates the full Big Data pipeline lifecycle:

Streaming ingestion (Kafka)
Real-time processing (Spark Structured Streaming)
Data lake storage (Parquet)
Persistent storage (PostgreSQL)
Machine learning (scikit-learn)
API serving (FastAPI)
Visualization (Streamlit)

Key Learning Outcomes
Designing real-time streaming pipelines
Running Spark on Windows using WSL2
Managing data lakes and relational storage together
Training and serving ML models from streaming data
Building interactive dashboards for analytics

### 📄 Technologies Used

Python · Pandas · scikit-learn · Kafka · Docker · PySpark · FastAPI · Uvicorn · Streamlit · PostgreSQL · Parquet · WSL2
---


