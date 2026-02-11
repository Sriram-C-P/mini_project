import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier


data = pd.read_csv('dataset.csv')
X = data.drop('Result', axis=1)
y = data['Result']


model = RandomForestClassifier()
model.fit(X, y)


importances = model.feature_importances_
feature_names = X.columns
feature_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False).head(10)


plt.figure(figsize=(10, 6))
sns.barplot(x=feature_imp, y=feature_imp.index)
plt.title("Top 10 Features for Phishing Detection (Our Analysis)")
plt.xlabel("Importance Score")
plt.show()