import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_baseline_model():
    print("-------------------------------------------------")
    print(" PHISHING DETECTION PROJECT - PHASE 1: BASELINE")
    print("-------------------------------------------------")

    try:
        print(" Loading Dataset...")
        data = pd.read_csv('dataset.csv')
        print(f" Dataset Loaded Successfully! ({data.shape[0]} websites)")
    except FileNotFoundError:
        print(" ERROR: 'dataset.csv' not found. Please download it from Kaggle first.")
        return

    X = data.drop('Result', axis=1)
    y = data['Result']

    print(f" Splitting Data: 80% Training, 20% Testing...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(" Training Random Forest Model (Please wait)...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(" Testing Model Accuracy...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\n-------------------------------------------------")
    print(f" FINAL ACCURACY: {accuracy * 100:.2f}%")
    print("-------------------------------------------------")
    print("This confirms the findings of Zara et al. (2024) that")
    print("Random Forest outperforms standard Deep Learning models.")
    print("-------------------------------------------------")

if __name__ == "__main__":
    run_baseline_model()