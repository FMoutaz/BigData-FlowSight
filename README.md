# FlowSight — Real-Time Traffic Congestion Forecasting Pipeline

FlowSight is an end-to-end real-time traffic analytics and forecasting pipeline built as a Big Data course project (ICS‑474).  
It simulates live traffic sensor events, ingests them with Kafka, processes streams with Spark (or a pure‑Python consumer), stores data in a Parquet data lake and PostgreSQL, trains a machine learning model, and serves predictions via a REST API. It also includes an interactive Streamlit dashboard for visualization.

This repository is based on: https://github.com/khush-i97/FlowSight

---

## ✨ Highlights

- Real-time traffic simulation and ingestion with Kafka
- Stream processing using PySpark Structured Streaming (or a Python consumer)
- Parquet-based data lake (bronze layer)
- Persistent storage in PostgreSQL
- Traffic speed forecasting with a Random Forest regressor
- REST API for live predictions using FastAPI
- Interactive dashboard with Streamlit (map visualization)

---

## ⚙️ Prerequisites

- Python 3.10+
- Java 17 (Temurin or Oracle JDK) — required by Spark
- Apache Spark 3.4+ (used via PySpark; WSL2 recommended on Windows)
- Docker Desktop (for Kafka, Zookeeper, PostgreSQL)
- WSL2 (Ubuntu) — recommended for running Spark on Windows
- Git

---

## 🚀 Quick setup

1. Clone the repository and enter the project folder:
```bash
git clone https://github.com/FMoutaz/BigData-FlowSight.git
cd BigData-FlowSight/FlowSight-upstream
```

2. Create virtual environments and install dependencies.

Windows (Producer, API, Dashboard)
```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

WSL / Ubuntu (Spark Structured Streaming)
```bash
python3 -m venv venv_wsl
source venv_wsl/bin/activate
pip install -r requirements.txt
```

Note: Virtual environments, generated data, and checkpoints are excluded from version control.

---

## 🧩 Pipeline — step by step

1. Start Kafka & Zookeeper (Docker)
```bash
docker compose -f docker-compose.yaml up -d
docker ps
```
- Kafka: localhost:9092
- Zookeeper: localhost:2181

2. Start PostgreSQL (Docker)
```bash
docker compose -f docker-compose.storage.yaml up -d
docker ps
```
- PostgreSQL: localhost:5432

3. Simulate traffic data (Producer)
```bash
python producer.py
```
This continuously publishes synthetic traffic sensor events to the Kafka topic `traffic`.

4. Stream to Bronze Layer (Spark Structured Streaming — run in WSL)
```bash
python stream_to_parquet.py
```
- Consumes Kafka `traffic` topic
- Writes streaming data to `data/bronze/`
- Uses checkpointing in `checkpoint/bronze/`
- Runs continuously to append Parquet files in real time

(If you prefer not to run Spark, there is a simple Python consumer alternative in the repo.)

5. Train the machine learning model
```bash
python train_model.py
```
- Trains a RandomForest regressor on historical data (Parquet)
- Saves the trained model as `model.joblib`

Example training summary (project sample)
- Parquet files used: 351
- Training samples: 921
- Testing samples: 231
- Mean Absolute Error (MAE): 14.13

6. Launch the FastAPI service
```bash
python -m uvicorn app:app --reload
```
Open API docs: http://127.0.0.1:8000/docs

Sample /predict request:
```json
{
  "sensor": "roadA",
  "speed": 48.3,
  "timestamp": 1627810200
}
```

Sample response:
```json
{
  "predicted_speed_next": 50.1
}
```

7. Run the Streamlit dashboard
```bash
# If the streamlit.exe launcher is unreliable:
python -m streamlit run dashboard.py

# Or normally:
streamlit run dashboard.py
```
Dashboard available at: http://localhost:8501

8. (Optional) Verify PostgreSQL storage
```bash
docker exec -it flowsight-upstream-postgres-1 \
  psql -U flowsight -d flowsight_db \
  -c "SELECT * FROM traffic_events LIMIT 5;"
```

---

## 🔎 What the dashboard shows

- Real-time and historical traffic trends per sensor
- Map visualization of sensor locations and current congestion
- Prediction controls to test the model with custom inputs

Screenshot:
![dashboard screenshot](https://github.com/user-attachments/assets/4678c6b3-614b-4b76-b266-740d9b467659)

---

## 📚 Key learning outcomes

- Designing and operating real-time streaming pipelines
- Running Spark on Windows using WSL2
- Managing data lakes (Parquet) alongside relational storage (Postgres)
- Training and serving ML models from streaming data
- Building interactive dashboards for analytics

---

## 🧰 Technologies used

Python · Pandas · scikit-learn · Kafka · Docker · PySpark · FastAPI · Uvicorn · Streamlit · PostgreSQL · Parquet · WSL2

---

## ⚠️ Troubleshooting & Tips

- If Spark fails on Windows, use WSL2 or run Spark on a Linux machine.
- Ensure Docker Desktop resources (CPU/memory) are sufficient for Kafka and Postgres.
- Check logs for each service (Docker container logs, uvicorn output, Spark console) for runtime issues.

---



