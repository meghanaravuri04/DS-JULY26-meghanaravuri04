import os
from src.data_loader import load_data
from src.data_cleaner import clean_data, save_cleaned_data

def run_pipeline():
    """Main execution entry point to process raw data into cleaned dataset."""
    raw_path = os.path.join('data', 'raw', 'logistics_data.csv')
    cleaned_path = os.path.join('data', 'cleaned', 'logistics_cleaned.csv')
    
    print("Loading raw data...")
    df_raw = load_data(raw_path)
    
    print("Checking data quality.")
    print(f"Raw records loaded: {len(df_raw)}")
    
    print("Cleaning data...")
    print("Applying business rules...")
    print("Creating derived columns...")
    df_cleaned = clean_data(df_raw)
    
    print("Saving cleaned data...")
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    save_cleaned_data(df_cleaned, cleaned_path)
    
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()