import json
import os
import time
import psycopg2
from kafka import KafkaConsumer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "127.0.0.1:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "traffic")

PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB   = os.getenv("PG_DB", "flowsight_db")
PG_USER = os.getenv("PG_USER", "flowsight")
PG_PASS = os.getenv("PG_PASS", "flowsight")

def main():
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS
    )
    conn.autocommit = True

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[BOOTSTRAP],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda v: v.decode("utf-8", errors="ignore"),
    )

    print(f"Consuming from topic={TOPIC} bootstrap={BOOTSTRAP} → Postgres {PG_HOST}:{PG_PORT}/{PG_DB}")

    with conn.cursor() as cur:
        for msg in consumer:
            raw = msg.value
            try:
                data = json.loads(raw)
            except Exception:
                data = {}

            event_ts = data.get("timestamp") or data.get("ts") or int(time.time())
            sensor = data.get("sensor") or data.get("road") or data.get("id") or "unknown"
            speed = data.get("speed") or data.get("value") or None

            cur.execute(
                """
                INSERT INTO traffic_events (event_ts, sensor, speed, raw)
                VALUES (%s, %s, %s, %s::jsonb)
                """,
                (int(event_ts), str(sensor), speed, json.dumps(data)),
            )

if __name__ == "__main__":
    main()
