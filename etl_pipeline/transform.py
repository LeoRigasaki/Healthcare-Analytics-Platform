import pandas as pd
import os
from datetime import datetime

def load_raw_data(file_path: str) -> pd.DataFrame:
    """Load the raw CSV data."""
    try:
        print(f"Attempting to load data from {file_path}...")
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        print(f"Error while loading data: {e}")
        raise RuntimeError(f"Failed to load data: {e}")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform data cleaning and preprocessing."""
    print("Starting data cleaning...")

    # Initial state of the DataFrame
    print(f"Initial data shape: {df.shape}")

    # Drop rows with missing critical information
    print("Dropping rows with missing 'locationname' or 'data_value'...")
    df = df.dropna(subset=['locationname', 'data_value'])
    print(f"Data shape after dropping rows: {df.shape}")

    # Fill missing values in 'geolocation' with 'Unknown'
    print("Filling missing 'geolocation' values with 'Unknown'...")
    df.loc[:, 'geolocation'] = df['geolocation'].fillna('Unknown')

    # Standardize column names
    print("Standardizing column names...")
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    # Ensure numeric columns have the correct type
    numeric_columns = ['data_value', 'low_confidence_limit', 'high_confidence_limit', 'totalpopulation', 'totalpop18plus']
    for col in numeric_columns:
        print(f"Converting column '{col}' to numeric type...")
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')

    # Drop duplicates
    print("Dropping duplicate rows...")
    df = df.drop_duplicates()
    print(f"Data shape after cleaning: {df.shape}")

    # Drop columns with all null values
    print("Dropping fully null columns 'data_value_footnote_symbol' and 'data_value_footnote'...")
    df = df.drop(columns=['data_value_footnote_symbol', 'data_value_footnote'])

    # Extract longitude and latitude from geolocation
    print("Extracting 'longitude' and 'latitude' from 'geolocation'...")
    df['longitude'] = df['geolocation'].str.extract(r'POINT \((-?\d+\.\d+)')[0].astype(float)
    df['latitude'] = df['geolocation'].str.extract(r'(-?\d+\.\d+)\)')[0].astype(float)

    print("Data cleaning complete.")
    return df

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns for additional insights."""
    print("Adding derived columns...")

    # Calculate the percentage of the population affected by the measure
    print("Calculating 'percentage_of_population'...")
    df['percentage_of_population'] = (df['data_value'] / df['totalpopulation']) * 100

    # Add a cleaned 'year_category' column for grouping
    print("Creating 'year_category' column...")
    df['year_category'] = df['year'].astype(str) + " - " + df['category']

    print("Derived columns added.")
    return df

def save_cleaned_data(df: pd.DataFrame, output_dir: str) -> str:
    """Save the cleaned dataset to a CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"cleaned_data_{timestamp}.csv")
    try:
        print(f"Saving cleaned data to {output_path}...")
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved successfully to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error while saving data: {e}")
        raise RuntimeError(f"Failed to save cleaned data: {e}")

if __name__ == "__main__":
    # Define paths
    raw_data_path = "./data/raw/cdc_data_20241226_185428.csv"  # Update to match your file
    output_dir = "./data/processed/"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        print("Starting the transformation pipeline...")

        # Load raw data
        print("Loading raw data...")
        raw_data = load_raw_data(raw_data_path)

        # Clean the data
        print("Cleaning the data...")
        cleaned_data = clean_data(raw_data)

        # Add derived columns
        print("Adding derived columns...")
        transformed_data = add_derived_columns(cleaned_data)

        # Save cleaned data
        print("Saving transformed data...")
        save_cleaned_data(transformed_data, output_dir)

        print("Transformation pipeline completed successfully.")

    except Exception as e:
        print(f"Transformation pipeline failed: {e}")
