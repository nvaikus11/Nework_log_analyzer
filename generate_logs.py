import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs():
    devices = ["Router_A", "Router_B", "Switch_X", "Switch_Y"]
    logs = []

    for _ in range(10):  # Generate 10 log entries
        device = random.choice(devices)
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))  # Random timestamps
        status = "ON" if random.random() > 0.3 else "OFF"  # 70% ON, 30% OFF

        logs.append({"Device": device, "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"), "Status": status})

    df = pd.DataFrame(logs)
    df.to_csv("data/network_logs.csv", index=False)
    print("Generated logs saved to data/network_logs.csv")

generate_logs()
