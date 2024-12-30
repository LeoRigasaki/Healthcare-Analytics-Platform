import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
import glob
import joblib
import matplotlib.pyplot as plt

# Load cleaned data
def load_cleaned_data(file_path: str) -> pd.DataFrame:
    """Load the cleaned dataset."""
    try:
        print(f"Loading cleaned data from {file_path}...")
        df = pd.read_csv(file_path)
        print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")

# Build predictive model
def build_and_evaluate_model(df: pd.DataFrame):
    """Build and evaluate a predictive model."""
    print("Starting predictive modeling...")

    # Select features and target
    features = ['year', 'category', 'totalpopulation']
    target = 'data_value'

    # Ensure no missing values in selected columns
    df = df.dropna(subset=features + [target])

    # Split data into training and testing sets
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocessing pipeline for numerical and categorical features
    numeric_features = ['year', 'totalpopulation']
    categorical_features = ['category']

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Define a simple model pipeline (Linear Regression or Random Forest)
    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])

    # Train the model
    print("Training the model...")
    model_pipeline.fit(X_train, y_train)

    # Make predictions
    y_pred = model_pipeline.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Model Evaluation:\nMSE: {mse:.2f}\nR2 Score: {r2:.2f}")

    # Save the model
    model_path = "./analytics/predictive_model.pkl"
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved successfully to {model_path}")

    # Save predictions
    predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    predictions.to_csv("./data/processed/predictions.csv", index=False)
    print("Predictions saved to ./data/processed/predictions.csv")

    # Plot actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, edgecolor='k')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--', color='red')
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title("Actual vs. Predicted Data Value")
    plt.show()

    return model_pipeline

if __name__ == "__main__":
    # Find the latest cleaned data file dynamically
    processed_dir = "./data/processed/"
    files = glob.glob(f"{processed_dir}cleaned_data_*.csv")
    if not files:
        raise RuntimeError("No cleaned data file found in the processed directory.")
    cleaned_data_path = max(files, key=os.path.getctime)
    print(f"Using latest cleaned data file: {cleaned_data_path}")

    # Load data
    cleaned_data = load_cleaned_data(cleaned_data_path)

    # Build and evaluate the predictive model
    model = build_and_evaluate_model(cleaned_data)

    print("Predictive modeling completed.")
