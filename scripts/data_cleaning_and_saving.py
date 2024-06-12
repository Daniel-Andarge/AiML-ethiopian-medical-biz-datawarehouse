import os
import pandas as pd
import re
import logging
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(filename='data_cleaning.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load environment variables
telegram_api_id = os.getenv('TELEGRAM_API_ID')
telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
telegram_phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')  
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
csv_directory = os.getenv('CSV_DIRECTORY')

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loaded data from {file_path} successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to load data from {file_path}: {e}")
        raise

def remove_duplicates(df):
    """Remove duplicate rows."""
    df_cleaned = df.drop_duplicates()
    logging.info("Removed duplicates.")
    return df_cleaned


def handle_missing_values(df):
    """Handle missing values."""
    try:
        # Fill missing values in 'content' column
        df['content'] = df['content'].fillna('message not found')
        
        # Drop rows with missing values in these columns
        columns_to_check = ['channel', 'message_id', 'message_link', 'timestamp', 'views']
        df.dropna(subset=columns_to_check, inplace=True)
        
        logging.info("Handled missing values.")
        return df
    except Exception as e:
        logging.error(f"Error handling missing values: {e}")
        raise



def standardize_formats(df):
    """Standardize formats."""
    df['content'] = df['content'].str.lower()
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S%z')
    logging.info("Standardized formats.")
    return df




def store_cleaned_data(df, file_path):
    """Store cleaned data to a CSV file."""
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Stored cleaned data to {file_path} successfully.")
    except Exception as e:
        logging.error(f"Failed to store cleaned data to {file_path}: {e}")
        raise

def save_to_database(df, table_name):
    """Save DataFrame to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        for index, row in df.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO {} (channel, message_id, content, timestamp, views, message_link)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING
            """).format(sql.Identifier(table_name))
            cursor.execute(insert_query, (row['channel'], row['message_id'], row['content'], row['timestamp'], row['views'], row['message_link']))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f'Saved {len(df)} records to {table_name}')
    except psycopg2.DatabaseError as e:
        logging.error(f'Database error: {e}')
    except Exception as e:
        logging.error(f'Error saving data to database: {e}')

def main():
    try:
        # Define file paths
        raw_data_path = os.path.join(csv_directory, 'Doctors Ethiopia.csv')
        cleaned_data_path = os.path.join(csv_directory, 'cleaned_data_Doctors Ethiopia.csv')
        
        # Load raw data
        df = load_data(raw_data_path)
        
        # Clean data
        df = remove_duplicates(df)
        df = handle_missing_values(df)
        df = standardize_formats(df)
        #df = validate_data(df)
        
        # Store cleaned data
        store_cleaned_data(df, cleaned_data_path)
        
        # Save cleaned data to database
        save_to_database(df, 'telegram_messages')
        
        logging.info("Data cleaning and loading process completed successfully.")
    except Exception as e:
        logging.error(f"Data cleaning and loading process failed: {e}")

if __name__ == "__main__":
    main()
