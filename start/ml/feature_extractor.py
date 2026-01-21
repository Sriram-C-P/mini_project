import numpy as np
from urllib.parse import urlparse
import whois
from datetime import datetime
import joblib
import warnings

warnings.filterwarnings("ignore")

MODEL_FILE = "hybrid_model.pkl"
EXPECTED_FEATURES = 31  


def get_url_features(url):
    print(f"[*] Extracting features for: {url}")

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc


    url_length = len(url)
    feat_url_len = 1 if url_length > 54 else -1


    feat_at_symbol = 1 if "@" in url else -1


    feat_https = -1 if parsed_url.scheme == "https" else 1


    print("    -> Checking Domain Age (WHOIS)...")
    try:
        domain_info = whois.whois(hostname)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            if creation_date.tzinfo is not None:
                creation_date = creation_date.replace(tzinfo=None)

            age_days = (datetime.now() - creation_date).days
            print(f"    -> Domain Age: {age_days} days")
            feat_domain_age = 1 if age_days < 180 else -1
        else:
            feat_domain_age = 1 

    except Exception as e:
        print(f"    -> WHOIS Lookup failed ({e}). Assuming suspicious.")
        feat_domain_age = 1


    features = [
        feat_at_symbol,
        feat_url_len,
        feat_https,
        feat_domain_age
    ]


    while len(features) < EXPECTED_FEATURES:
        features.append(0)

    return np.array([features])


def scan_url(url):
    features_array = get_url_features(url)

    try:
        model = joblib.load(MODEL_FILE)

        prediction = model.predict(features_array)
        probabilities = model.predict_proba(features_array)

        if prediction[0] == 1:
            result = "PHISHING"
            confidence = probabilities[0][1] * 100
        else:
            result = "LEGITIMATE"
            confidence = probabilities[0][0] * 100

        print("-" * 40)
        print(f"FINAL RESULT : {result}")
        print(f"CONFIDENCE   : {confidence:.2f}%")
        print("-" * 40)

    except FileNotFoundError:
        print(f"[!] Error: '{MODEL_FILE}' not found.")
        print("    Run build_system.py first.")
    except Exception as e:
        print(f"[!] An error occurred: {e}")


if __name__ == "__main__":
    scan_url("https://google.com")
    print()
    scan_url("http://secure-login-update-account.com")
