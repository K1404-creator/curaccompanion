# neurotap_dataset.py
import numpy as np
import pandas as pd


def generate_neurotap_dataset(n_samples=1000, seed=42):
    np.random.seed(seed)
    
    data = []
    for _ in range(n_samples):
        # Randomly assign fatigue state
        fatigue = np.random.choice([0, 1], p=[0.6, 0.4])  # 60% alert, 40% fatigued

        if fatigue == 0:  # Alert
            avg_key_latency = np.random.normal(120, 20)    # ms
            error_rate = np.random.normal(0.02, 0.01)      # 2% errors
            backspace_rate = np.random.normal(0.05, 0.02)
            typing_speed = np.random.normal(65, 10)        # words per min
            session_duration = np.random.normal(15, 5)     # minutes
        else:  # Fatigued
            avg_key_latency = np.random.normal(200, 40)
            error_rate = np.random.normal(0.08, 0.03)      # 8% errors
            backspace_rate = np.random.normal(0.12, 0.05)
            typing_speed = np.random.normal(40, 8)
            session_duration = np.random.normal(45, 15)

        data.append([avg_key_latency, error_rate, backspace_rate,
                     typing_speed, session_duration, fatigue])

    df = pd.DataFrame(data, columns=[
        "avg_key_latency", "error_rate", "backspace_rate",
        "typing_speed", "session_duration", "fatigue_label"
    ])

    return df


if __name__ == "__main__":
    df = generate_neurotap_dataset(500)
    print(df.head())
    df.to_csv("datasets/neurotap_synthetic.csv", index=False)