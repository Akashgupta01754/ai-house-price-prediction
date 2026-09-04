import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataset
data = pd.read_csv("housing.csv")

# Features
X = data[["area", "bedrooms", "bathrooms", "parking"]]

# Target
y = data["price"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Test
predictions = model.predict(X_test)

# Evaluation
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print("R2 Score:", round(r2, 4))
print("MAE:", round(mae, 2))

# Save model
joblib.dump(model, "house_price_model.pkl")

print("Model saved successfully!")