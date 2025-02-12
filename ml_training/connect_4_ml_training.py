import pandas as pd
import joblib
import gc
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
url = "connect-4.data"
column_names = [f"col_{i}" for i in range(42)] + ["outcome"]  # Ensure correct column name

df = pd.read_csv(url, names=column_names, dtype="category")

# Map board values (fixing FutureWarning)
mapping = {'b': 0, 'x': 1, 'o': -1}
for col in df.columns[:-1]:
    df[col] = df[col].astype(str).map(mapping).astype("int8")  # Convert to str before mapping

# Map outcomes (fixing the error)
outcome_mapping = {'win': 1, 'loss': -1, 'draw': 0}
df["outcome"] = df["outcome"].astype(str).map(outcome_mapping).astype("int8")  # Explicit mapping

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df.iloc[:, :-1], df["outcome"], test_size=0.2, random_state=42
)

del df  # Free unused memory
gc.collect()

# Train Random Forest Classifier
model = RandomForestClassifier(
    n_estimators=90,
    max_depth=10,
    min_samples_split=5,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Optimized Model Accuracy: {accuracy:.4f}")

# Save the model
joblib.dump(model, "connect4_ml_agent.pkl", compress=3)

# Clean up
del X_train, X_test, y_train, y_test, model, y_pred
gc.collect()

print("Training complete. Model saved as 'connect4_ml_agent.pkl'")
