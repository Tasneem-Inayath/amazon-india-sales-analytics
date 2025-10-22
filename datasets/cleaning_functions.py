import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
import re

# question1:
def clean_order_date(df, date_column='order_date'):

    def parse_date(x):
        if pd.isna(x):
            return pd.NaT
        x = str(x).strip()  # remove whitespace
        # Try multiple known formats
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d-%m-%y", "%Y-%m-%d", "%Y/%m/%d"):
            try:
                return pd.to_datetime(datetime.strptime(x, fmt))
            except:
                continue
        # If none matches, return NaT
        return pd.NaT

    df[date_column] = df[date_column].apply(parse_date)
    
    # Standardize format to YYYY-MM-DD
    df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    
    return df
# question2:
def clean_original_price(df, price_column='original_price_inr'):

    def parse_price(x):
        if pd.isna(x):
            return pd.NA
        x = str(x).strip()  # remove spaces
        # Remove ₹ and commas
        x = re.sub(r'[₹,]', '', x)
        # Check if numeric
        if x.replace('.', '', 1).isdigit():
            return float(x)
        else:
            return pd.NA
    
    df[price_column] = df[price_column].apply(parse_price)
    
    return df
# question3:
def clean_customer_rating(df, rating_column='customer_rating'):

    def parse_rating(x):
        if pd.isna(x):
            return pd.NA
        x = str(x).strip()
        
        # Extract first numeric pattern (e.g., 4, 4.5)
        match = re.search(r'(\d+(\.\d+)?)', x)
        if match:
            val = float(match.group(1))
            # Keep only valid 0–5 ratings
            if 0 <= val <= 5:
                return val
        return pd.NA
    
    df[rating_column] = df[rating_column].apply(parse_rating)
    return df
# question4:
def clean_customer_city(df):
    """
    Dynamically standardize city names in the 'customer_city' column.
    Handles variations, slashes, casing, and spelling errors.
    """
    if 'customer_city' not in df.columns:
        print("Warning: 'customer_city' column not found.")
        return df

    def normalize_city_name(city):
        if pd.isna(city):
            return pd.NA
        
        # Lowercase for uniformity
        city = str(city).strip().lower()

        # Replace slashes, hyphens, extra spaces
        city = re.sub(r"[/\-]", " ", city)
        city = re.sub(r"\s+", " ", city)

        # Correct common variations dynamically
        replacements = {
            'bangalore': 'bengaluru',
            'bombay': 'mumbai',
            'delhi': 'new delhi',
            'madras': 'chennai',
            'calcutta': 'kolkata',
        }
        for old, new in replacements.items():
            if old in city:
                city = new

        # Capitalize first letter of each word
        return city.title()

    # Apply cleaning
    df['customer_city'] = df['customer_city'].apply(normalize_city_name)

    # Replace empty or invalid strings with pd.NA
    df['customer_city'] = df['customer_city'].replace(["", "na", "none", "null"], pd.NA)

    return df
# question5:
def clean_boolean_columns(df, bool_columns=None):
    """
    Standardize boolean columns to True/False and use pd.NA for missing/invalid entries.
    """
    if bool_columns is None:
        # Default columns to clean
        bool_columns = ['is_prime_member', 'is_prime_eligible', 'is_festival_sale']
    
    def to_boolean(x):
        if pd.isna(x):
            return pd.NA
        x_str = str(x).strip().lower()
        if x_str in ['true', '1', 'yes', 'y']:
            return True
        elif x_str in ['false', '0', 'no', 'n']:
            return False
        else:
            return pd.NA  # Anything else treated as missing

    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].apply(to_boolean)
    
    return df
# question6:
def clean_product_category(df, category_column='category'):
    """
    Standardize product category names:
    - Handles variations like 'Electronics', 'Electronic', 'ELECTRONICS', 'Electronicss'
    - Keeps consistent naming as either 'Electronics' or 'Electronics & Accessories'
    - Replaces missing or invalid values with pd.NA
    """

    def standardize_category(cat):
        if pd.isna(cat):
            return pd.NA
        cat = str(cat).strip().lower()

        if 'accessor' in cat:
            return 'Electronics & Accessories'
        elif cat in ['electronics', 'electronic', 'electronicss', 'electronics']:
            return 'Electronics'
        else:
            return cat.title()

    df[category_column] = df[category_column].apply(standardize_category)
    return df
# question7:
def clean_delivery_days(df, column_name='delivery_days'):

    def parse_delivery(value):
        if pd.isna(value):
            return pd.NA

        val = str(value).strip().lower()

        # Handle common text formats
        if val in ['same day', 'express']:
            return 0
        elif re.match(r'^\d+\s*-\s*\d+', val):        # '1-2 days'
            nums = [int(x) for x in re.findall(r'\d+', val)]
            return round(sum(nums) / len(nums))
        elif re.search(r'\d+', val):                  # '5' or '3 days'
            num = int(re.search(r'\d+', val).group()) #type: ignore
            return num if 0 <= num <= 30 else pd.NA
        else:
            return pd.NA

    df[column_name] = df[column_name].apply(parse_delivery).astype('Int64')
    return df
# question8:
def handle_duplicates(df):
    key_cols =['customer_id', 'order_date', 'product_id','final_amount_inr']
    dup_count = df.duplicated(subset=key_cols,keep =False)
    duplicates  = df[dup_count]
    def resolve_duplicates(group):
        if group['quantity'].sum() > group['quantity'].iloc[0]:
            return group
        else:
            return group.iloc[0]
    df_cleaned = duplicates.groupby(key_cols,group_keys = False).apply(resolve_duplicates)
    df_non_duplicates = df[~dup_count]
    df_final = pd.concat([df_cleaned, df_non_duplicates], ignore_index=True)
    return df_final
# question9:
def handle_outlier_prices_domain1(df, price_col='original_price_inr', category_col='category', factor_high=100, factor_low=0.01):

    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    
    # Calculate median price per category
    category_median = df.groupby(category_col)[price_col].transform('median')
    
    # Replace unrealistic high prices
    df[price_col] = np.where(df[price_col] > factor_high * category_median, category_median, df[price_col])
    
    # Replace unrealistic low prices
    df[price_col] = np.where(df[price_col] < factor_low * category_median, category_median, df[price_col])
    
    return df

# question9 improved:
import pandas as pd
import numpy as np

def handle_outlier_prices_domain(df, price_col='original_price_inr', category_col='category', factor_high=100, factor_low=0.01):
    """
    Identify and correct unrealistic price outliers using per-category median-based domain logic.
    Also prints summary of outliers before correction.
    """
    # Ensure both required columns exist
    if price_col not in df.columns or category_col not in df.columns:
        print(f"❌ Missing required columns: {price_col} or {category_col}")
        return df

    # Step 1: Convert price column to numeric safely
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')

    # Step 2: Compute per-category median
    category_median = df.groupby(category_col)[price_col].transform('median')

    # Handle cases where median could be NaN
    category_median = category_median.fillna(df[price_col].median())

    # Step 3: Detect outliers before correction
    high_mask = df[price_col] > factor_high * category_median
    low_mask = df[price_col] < factor_low * category_median

    high_outliers = df[high_mask]
    low_outliers = df[low_mask]

    print(f"High outliers detected: {len(high_outliers)}")
    print(f"Low outliers detected: {len(low_outliers)}")

    if not high_outliers.empty:
        print("\nSample high outliers:")
        print(high_outliers[[category_col, price_col]].head())

    if not low_outliers.empty:
        print("\nSample low outliers:")
        print(low_outliers[[category_col, price_col]].head())

    # Step 4: Replace unrealistic values with category median
    df.loc[high_mask, price_col] = category_median[high_mask]
    df.loc[low_mask, price_col] = category_median[low_mask]

    print("\n✅ Outlier correction complete.\n")
    return df

# question10:
import re

def clean_payment_methods(df, column='payment_method'):
    """
    Standardize payment method names and ensure consistent categorical naming.
    """
    if column not in df.columns:
        print(f"❌ Column '{column}' not found in DataFrame.")
        return df

    # Convert to lowercase and strip spaces
    df[column] = df[column].astype(str).str.lower().str.strip()

    # Define mapping patterns
    payment_mapping = {
        r'\bupi\b|\bphonepe\b|\bgoogle\s?pay\b|\bpaytm\b|\bbhim\b': 'UPI',
        r'\bcredit\s?card\b|\bcreditcard\b|\bcc\b|\bmastercard\b|\bvisa\b': 'Credit Card',
        r'\bdebit\s?card\b|\bdebitcard\b': 'Debit Card',
        r'\bcash\s?on\s?delivery\b|\bcod\b|\bc\.o\.d\b': 'Cash on Delivery',
        r'\bnet\s?banking\b|\bonline\s?banking\b': 'Net Banking',
        r'\bwallet\b': 'Wallet',
        r'\bemi\b': 'EMI',
    }

    # Apply replacements
    for pattern, replacement in payment_mapping.items():
        df[column] = df[column].apply(lambda x: replacement if re.search(pattern, x) else x)

    # Convert to title case for consistency
    df[column] = df[column].str.title()

    # Optional: print summary
    print("\n✅ Payment method cleaning complete. Unique values after cleaning:")
    print(df[column].unique())

    return df

# final function to clean all datasets in a directory
def clean_all_amazon_datasets(input_folder, output_folder):
    """
    Loop through all CSV files in input_folder, clean them using all cleaning functions,
    and save cleaned files in output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    for file in csv_files:
        print(f"Cleaning dataset: {file}")
        df = pd.read_csv(file)
        
        # --- Apply all cleaning functions sequentially ---
        df = clean_order_date(df)
        df = clean_original_price(df)
        df = clean_customer_rating(df)
        df = clean_customer_city(df)
        df = clean_boolean_columns(df)
        df = clean_product_category(df)
        df = clean_delivery_days(df)
        df = handle_duplicates(df)
        df = handle_outlier_prices_domain1(df)
        df = clean_payment_methods(df)
        
        # Save cleaned dataset
        base_name = os.path.basename(file)
        output_path = os.path.join(output_folder, base_name)
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned dataset: {output_path}")

clean_all_amazon_datasets("datasets/", "cleaned_datasets/")