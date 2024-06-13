import os
import psycopg2
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')  

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# connect to PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        logger.info("Connected to PostgreSQL database")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        raise

# Function to save detection results into database
def save_to_db(conn, class_label, x_center, y_center, width, height, confidence):
    try:
        cur = conn.cursor()
        sql = "INSERT INTO yolo_detection_results (class_label, x_center, y_center, width, height, confidence) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (class_label, x_center, y_center, width, height, confidence)
        cur.execute(sql, values)
        conn.commit()
        logger.info(f"Saved detection result for class {class_label} to database")
        cur.close()
    except psycopg2.Error as e:
        logger.error(f"Error saving to PostgreSQL: {e}")
        raise


result_dir = '../yolov5/results/run13/labels'

try:
    # Connect to PostgreSQL
    conn = connect_to_db()

    # Iterat
    for filename in os.listdir(result_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(result_dir, filename)
            
            # Read contents of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Process each line in the file
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 6:
                    class_label = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                    confidence = float(parts[5])
                    
                    # Save to database
                    save_to_db(conn, class_label, x_center, y_center, width, height, confidence)

    print("Detection results saved to database.")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
finally:
    if conn is not None:
        conn.close()
        logger.info("PostgreSQL connection closed")
