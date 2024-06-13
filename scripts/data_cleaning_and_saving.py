import os
import pandas as pd
import re
import logging
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# Logging configuration
logging.basicConfig(filename='data_cleaning.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load environment variables
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')  
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


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
    df['content'] = df['content'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
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

        # Create the table if it doesn't exist
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                channel TEXT,
                message_id INT,
                content TEXT,
                timestamp TIMESTAMP WITH TIME ZONE,
                views FLOAT,
                message_link TEXT
            )
        """).format(sql.Identifier(table_name))
        cursor.execute(create_table_query)

        for index, row in df.iterrows():
    
            select_query = sql.SQL("""
                SELECT 1 FROM {} WHERE message_id = %s
            """).format(sql.Identifier(table_name))
            cursor.execute(select_query, (row['message_id'],))
            if cursor.fetchone():
                update_query = sql.SQL("""
                    UPDATE {} SET
                        channel = %s,
                        content = %s,
                        timestamp = %s,
                        views = %s,
                        message_link = %s
                    WHERE message_id = %s
                """).format(sql.Identifier(table_name))
                cursor.execute(update_query, (row['channel'], row['content'], row['timestamp'], row['views'], row['message_link'], row['message_id']))
            else:
           
                insert_query = sql.SQL("""
                    INSERT INTO {} (channel, message_id, content, timestamp, views, message_link)
                    VALUES (%s, %s, %s, %s, %s, %s)
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
        raw_csv_directory = os.getenv('CSV_DIRECTORY')
        cleaned_CSV_directory = os.getenv('CLEANED_CSV_DIRECTORY')

        # list to store the  DataFrames
        standardized_dfs = []

        # Iterate over raw_csv_directory
        for filename in os.listdir(raw_csv_directory):
            if filename.endswith('.csv'):
                raw_data_path = os.path.join(raw_csv_directory, filename)
                df = load_data(raw_data_path)
                standardized_df = standardize_formats(df)
                standardized_dfs.append(standardized_df)

        # combine dataframes
        combined_df = pd.concat(standardized_dfs, ignore_index=True)

        # Clean and store the data
        combined_df = remove_duplicates(combined_df)
        combined_df = handle_missing_values(combined_df)


        # Define the cleaned data path
        cleaned_data_path = os.path.join(cleaned_CSV_directory, 'cleaned_data.csv')

        # Store cleaned data
        store_cleaned_data(combined_df, cleaned_data_path)

        # Save cleaned data to database
        save_to_database(combined_df, 'telegram_messages')

        logging.info("Data cleaning and loading process completed successfully.")
    except Exception as e:
        logging.error(f"Data cleaning and loading process failed: {e}")

if __name__ == "__main__":
    main()
