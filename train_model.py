import numpy as np 
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load Dataset
heart_disease = pd.read_csv('Heart.csv')

# Splitting features and target
x = heart_disease.drop(columns='target', axis=1)
y = heart_disease['target']

# Split data into training and testing
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=2
)

# Model Training
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

# Accuracy
train_accuracy = accuracy_score(model.predict(x_train), y_train)
test_accuracy = accuracy_score(model.predict(x_test), y_test)

# Save Model + Accuracy
model_data = {
    "model": model,
    "train_accuracy": train_accuracy,
    "test_accuracy": test_accuracy
}

with open("heart_model.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("Model & Accuracy Saved Successfully ✅")
