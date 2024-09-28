# Ethiopian Medical Data Warehouse and Analytics Pipeline
The Ethiopian Medical Business Data Warehouse & Analytics Platform aims to enhance the efficiency of Ethiopia's healthcare sector by creating a robust data warehouse. The project will extract data and images from public Telegram channels related to Ethiopian medical businesses, perform object detection on the images, and clean, transform, and store the extracted data in the warehouse. The main goal is to provide a unified solution for data analysis, supporting informed decision-making and driving strategic advancements in healthcare.

### Technologies/Tools Used:
Python, DBT, SQL, ETL, PostgreSQL, FastAPI, Pandas, Pytest, SQLAlchemy, YOLOv5 Postman, CI/CD, Jupiter Notebook,Git , PDF & Google Drive (for project report).

### Key Accomplishments

- **ETL Process:** Successfully managed the end-to-end ETL process, including data extraction, cleaning, transformation, and loading.
  
 - **DBT for Data Modeling:** Implemented data modeling and transformation using SQL with DBT.

- **Image Extraction and Object Detection:** Extracted images from Telegram channels, performed object detection, and stored the results back into the data warehouse.

- **Database Management:** Loaded cleaned data into a PostgreSQL database.

- **API Development:** Exposed cleaned data for analysis through APIs using FastAPI, facilitating easy access from the database/data warehouse.
  
- **Project Documentation:** Prepared comprehensive documentation for each step of the project to ensure clarity and understanding for the client.

## Table of Contents

1. [Data Scraping and Collection Pipeline](#data-scraping-and-collection-pipeline)
2. [Data Cleaning and Transformation](#data-cleaning-and-transformation)
3. [Object Detection Using YOLO](#object-detection-using-yolo)
4. [Exposing the Collected Data Using FastAPI](#exposing-the-collected-data-using-fastapi)
5. [Postman Collection](#postman-collection)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Contributing](#contributing)
9. [License](#license)

## Data Scraping and Collection Pipeline

### Telegram Scraping

Utilize the Telegram API or custom scripts to extract data from public Telegram channels related to Ethiopian medical businesses. Key channels include:

![scraped](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/scraped_data.png)

### Image Scraping

Collect images from specified Telegram channels for object detection:

- [Chemed Telegram Channel](https://t.me/lobelia4cosmetics)
- [Lobelia for Cosmetics](https://t.me/lobelia4cosmetics)

For more details, see the [data_scraping_and_cleaning.ipynb](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/tree/main/notebooks/data_scraping_and_cleaning.ipynb) notebook.

## Data Cleaning and Transformation

### Data Cleaning

- Remove duplicates
- Handle missing values
- Standardize formats
- Validate data

### Data Cleaning Models DBT Doc

Set up DBT for data transformation and create models (SQL files) for data transformation:

```sh
pip install dbt
dbt init dbt_med
dbt run
```

![dbt](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/dbt%20Docs_models.jpg)

### Storing Cleaned Data

Store cleaned data in a database.

![dbt_db](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/dbt%20Docs_database.jpg)

### Fact Table in PostgreSQL Database

![dbt_db](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/fact_table.png)

For more details, see the [data_scraping_and_cleaning.ipynb](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/tree/main/notebooks/data_scraping_and_cleaning.ipynb) notebook.

## Object Detection Using YOLO

### Setting Up the Environment

Ensure necessary dependencies are installed:

```sh
pip install opencv-python
pip install torch torchvision
pip install tensorflow
```

### Downloading the YOLO Model

```sh
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

### Preparing the Data

- Collect images from the specified Telegram channels.
- Use the pre-trained YOLO model to detect objects in the images.

### Processing the Detection Results

- Extract data such as bounding box coordinates, confidence scores, and class labels.
- Store detection data in a database table.

![yolo](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/table_yolo_detection.png)

For more details, see the [yolo.ipynb](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/tree/main/notebooks/yolo.ipynb) notebook.

## Exposing the Collected Data Using FastAPI

### Setting Up the Environment

Install FastAPI and Uvicorn:

```sh
pip install fastapi uvicorn
```

### Create a FastAPI Application

Set up a basic project structure:

```
my_project/
├── main.py
├── database.py
├── models.py
├── schemas.py
└── crud.py
```

### Database Configuration

- In `database.py`, configure the database connection using SQLAlchemy.

### Creating Data Models

- In `models.py`, define SQLAlchemy models for the database tables.

### Creating Pydantic Schemas

- In `schemas.py`, define Pydantic schemas for data validation and serialization.

### CRUD Operations

- In `crud.py`, implement CRUD (Create, Read, Update, Delete) operations for the database.

### Creating API Endpoints

- In `main.py`, define the API endpoints using FastAPI.

![crud](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/fastapi_crud.png)

### Get All Telegram Data

![get](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_telegram_data.png)
![get](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_telegram_data2.png)

### Get All YOLO Detection Results

![getyolo](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_yolo_result.png)

## Postman Collection

You can use the Postman API collection found in the link below:

[Postman collection link](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/fastAPI/postman_collection/medicalAPI.postman_collection.json)

## Installation

To get started, follow these steps:

1. **Clone the repository**:

   ```sh
   git clone https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse.git
   cd AiML-ethiopian-medical-biz-datawarehouse
   ```

2. **Create a virtual environment and activate it**:

   ```sh
   # Using virtualenv
   virtualenv venv
   source venv/bin/activate

   # Using conda
   conda create -n your-env python=3.x
   conda activate your-env
   ```

3. **Install the required dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run Data Scraping Scripts**:

   ```sh
   python extract_load_pipeline.py
   ```

2. **Run DBT Models**:

   ```sh
   dbt run
   ```

3. **Run Object Detection**:

   ```sh
   python detect.py --source data/telegram_images --save-txt --save-conf --project results --name run1
   ```

4. **Start FastAPI Application**:

   ```sh
   uvicorn main:app --reload
   ```

## Contributing

Contributions are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Create a pull request to the main repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to the contributors and the open-source community for their support and resources.
