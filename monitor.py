# monitor.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import time
import csv
import numpy as np

DATA_PATH = "shared_data.csv"
LOG_PATH   = "log.csv"

# ---------------------
# Train realistic model
# ---------------------

def normal_point():
    # use realistic distributions
    pressure = np.random.normal(55, 3)
    temperature = 110 + (pressure - 55)*0.6 + np.random.normal(0, 2)
    ics_write = np.random.normal(4, 0.5)
    login_hr  = 9
    return [pressure, temperature, ics_write, login_hr]

train_df = pd.DataFrame(
    [normal_point() for _ in range(500)],
    columns=["pressure","temperature","ics_write","login_hour"]
)

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(train_df)

print("=== Real-Time OT Monitoring Started ===")

last_len = 0

while True:
    try:
        df = pd.read_csv(DATA_PATH, header=None,
            names=["pressure","temperature","ics_write","login_hour","source"])
    except:
        time.sleep(0.5)
        continue

    if len(df) == last_len:
        time.sleep(0.2)
        continue

    row = df.iloc[-1]
    features = pd.DataFrame([row[["pressure","temperature","ics_write","login_hour"]]], 
                            columns=["pressure","temperature","ics_write","login_hour"])
    pred = model.predict(features)[0]

    entry = row.to_dict()

    if pred == -1:
        print(f"🚨 ALERT — anomaly detected: {entry}")
        alert = 1
    else:
        print(f"[OK] {entry}")
        alert = 0

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            entry["pressure"], entry["temperature"], entry["ics_write"],
            entry["login_hour"], alert, entry["source"]
        ])

    last_len = len(df)
    time.sleep(0.2)
