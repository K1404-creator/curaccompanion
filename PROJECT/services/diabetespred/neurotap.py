# models/neurotap_model.py
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv(r"C:\Users\Krish\Documents\PROJECT\dataset\neurotap_synthetic.csv")

X = df.drop("fatigue_label", axis=1)
y = df["fatigue_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/neurotap_model.pkl")

print("Model trained. Accuracy:", model.score(X_test, y_test))