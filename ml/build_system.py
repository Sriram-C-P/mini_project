import pandas as pd
import numpy as np
import joblib
import os
import sys

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

DATA_FILE = 'dataset.csv'
MODEL_FILE = 'hybrid_model.pkl'

def initialize_system():
    print("--- SYSTEM INITIALIZATION ---")
    
    if not os.path.exists(DATA_FILE):
        print(f"[!] Error: {DATA_FILE} not found.")
        sys.exit()

    print(f"Loading {DATA_FILE}...")
    data = pd.read_csv(DATA_FILE)

    if 'id' in data.columns:
        data = data.drop(columns=['id'])

    X = data.drop('Result', axis=1)
    y = data['Result'].map({-1: 0, 1: 1}) 

    print(f"Training on {X.shape[1]} features.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

    model = VotingClassifier(estimators=[('rf', rf), ('xgb', xgb)], voting='soft')
    
    print("Training Hybrid Model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {acc*100:.2f}%")

    joblib.dump(model, MODEL_FILE)
    print(f"Success: Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    initialize_system()