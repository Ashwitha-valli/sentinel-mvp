import pandas as pd
from datetime import datetime
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), '../data/symptoms_log.csv')

def log_symptom(query: str, label: str):
    timestamp = datetime.now().isoformat()
    entry = {"timestamp": timestamp, "query": query, "symptom_label": label}
    try:
        df = pd.read_csv(LOG_PATH)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([entry])
    df.to_csv(LOG_PATH, index=False)
