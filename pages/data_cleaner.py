import pandas as pd
import numpy as np

def clean_redbull_data(df_raw):
    """Performs all data cleaning steps on the Red Bull sales DataFrame."""

    df = df_raw.copy()

    # 1. Handle Duplicate Data
    df = df.drop_duplicates()

    # 2. Handle Inconsistent Data
    # Standardize Region Column
    df['Region'] = df['Region'].str.strip().str.lower()
    region_mapping = {
        'th-central': 'TH-Central', 'th central': 'TH-Central',
        'thailand central': 'TH-Central', 'thailand-central': 'TH-Central',
        'thailand': 'TH-Central',
        'usa-east': 'USA-East', 'us east': 'USA-East',
        'united states east': 'USA-East', 'u.s.a.': 'USA-East',
        'europe-eu': 'Europe-EU', 'eu': 'Europe-EU',
        'europe': 'Europe-EU', 'european union': 'Europe-EU',
        'asia-pacific': 'Asia-Pacific', 'asia-pac': 'Asia-Pacific',
        'apac': 'Asia-Pacific', 'asia pacific': 'Asia-Pacific'
    }
    df['Region'] = df['Region'].replace(region_mapping)
    df['Region'] = df['Region'].str.upper()

    # Standardize Product_Variant Column
    df['Product_Variant'] = df['Product_Variant'].str.strip().str.lower()
    product_variant_mapping = {
        'original blue': 'Original Blue', 'original  blue': 'Original Blue',
        'krating daeng 250': 'Krating Daeng 250',
        'red edition': 'Red Edition',
        'sugarfree': 'Sugarfree', 'sugar free': 'Sugarfree',
        'sugarfree ': 'Sugarfree', 'sugar-free': 'Sugarfree',
        'tropical edition': 'Tropical Edition', 'tropical  edition': 'Tropical Edition',
        'tropical': 'Tropical Edition'
    }
    df['Product_Variant'] = df['Product_Variant'].replace(product_variant_mapping)

    # Standardize Channel Column
    df['Channel'] = df['Channel'].str.strip().str.lower()
    channel_mapping = {
        'social media': 'Social Media', 'social_media': 'Social Media',
        'tv ad': 'TV Ad', 'tv ads': 'TV Ad',
        'tv advertisement': 'TV Ad', 'television ad': 'TV Ad',
        'in-store promo': 'In-store Promo',
        'f1 sponsorship': 'F1 Sponsorship',
        'extreme sports': 'Extreme Sports'
    }
    df['Channel'] = df['Channel'].replace(channel_mapping)
    df['Channel'] = df['Channel'].apply(lambda x: x.title() if isinstance(x, str) else x)

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')

    # 3. Handle Missing Data
    median_marketing = df['Marketing_Spend'].median()
    df['Marketing_Spend'] = df['Marketing_Spend'].fillna(median_marketing)
    median_score = df['Customer_Score'].median()
    df['Customer_Score'] = df['Customer_Score'].fillna(median_score)

    # 4. Handle Noisy Data
    df = df[df['Unit_Price'] > 0]
    df = df[df['Units_Sold'] > 0]
    df = df[df['Marketing_Spend'] >= 0]
    df = df[(df['Customer_Score'] >= 1) & (df['Customer_Score'] <= 10)]

    # 5. Outlier Detection (No treatment applied as per notebook decision)
    # The notebook decided not to apply winsorization due to potential business logic issues.
    # Outlier detection can still be performed for informational purposes in Streamlit app
    # but no modification to the DataFrame is made here.

    return df

# Example usage (for testing or if this script is run standalone)
if __name__ == '__main__':
    # This part assumes you have 'redbull_workshop_dirty.csv' in the same directory
    try:
        df_dirty = pd.read_csv('redbull_workshop_dirty.csv')
        print(f"Raw data shape: {df_dirty.shape}")
        df_cleaned = clean_redbull_data(df_dirty)
        print(f"Cleaned data shape: {df_cleaned.shape}")
        print("First 5 rows of cleaned data:")
        print(df_cleaned.head())
        df_cleaned.to_csv('redbull_clean_from_function.csv', index=False)
        print("Cleaned data saved to redbull_clean_from_function.csv")
    except FileNotFoundError:
        print("Error: redbull_workshop_dirty.csv not found. Please ensure it's in the correct directory.")
