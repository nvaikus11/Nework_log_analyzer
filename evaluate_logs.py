import pandas as pd
from openai import OpenAI
from datetime import datetime

# Load OpenAI API Key
client = OpenAI(api_key="your_openai_api_key")

# Load golden rules
rules_df = pd.read_excel("data/golden_rules.xlsx")

# Load network logs
logs_df = pd.read_csv("data/network_logs.csv")

def check_device_status(device, last_seen):
    current_time = datetime.now()
    last_seen_time = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
    time_diff = (current_time - last_seen_time).total_seconds() / 60  # Minutes

    rule = rules_df[rules_df["Device Type"] == device.split("_")[0]]["Status Rule"].values
    if rule:
        expected_status = rule[0]
        if expected_status == "ON" and time_diff < 10:
            return "ON"
        elif expected_status == "OFF" and time_diff > 30:
            return "OFF"
    return "UNKNOWN"

logs_df["Evaluated_Status"] = logs_df.apply(lambda row: check_device_status(row["Device"], row["Timestamp"]), axis=1)
logs_df.to_csv("data/evaluated_logs.csv", index=False)
print("Evaluated logs saved to data/evaluated_logs.csv")

# Use GPT to summarize
prompt = f"Analyze this network log: {logs_df.to_string()}\nAre any devices down?"
response = client.completions.create(model="gpt-4", prompt=prompt, max_tokens=100)

print("\nGPT Evaluation:")
print(response.choices[0].text)
