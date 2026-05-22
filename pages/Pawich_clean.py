import pandas as pd

def load_cleaned_data(file_path='redbull_clean.csv'):
    """Loads the cleaned Red Bull sales data from a CSV file."""
    try:
        df_cleaned = pd.read_csv(file_path)
        print(f"Successfully loaded cleaned data from {file_path}. Shape: {df_cleaned.shape}")
        return df_cleaned
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please ensure it's in the correct directory.")
        return pd.DataFrame()

if __name__ == '__main__':
    # Example usage when running this script directly
    cleaned_df = load_cleaned_data()
    if not cleaned_df.empty:
        print("\nFirst 5 rows of the cleaned DataFrame:")
        print(cleaned_df.head())
