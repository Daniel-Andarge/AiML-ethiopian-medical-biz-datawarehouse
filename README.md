# Ethiopian Medical Business Data Warehouse & Data Pipeline

The Ethiopian Medical Business Data Warehouse & Analytics Platform is a comprehensive data solution designed to empower the Ethiopian healthcare and medical industry. This project aims to build a robust and scalable data warehouse that consolidates data from various sources, including medical facilities, pharmaceutical companies, insurance providers, and government agencies. By leveraging advanced analytics and business intelligence techniques, the platform will provide data-driven insights to support decision-making, improve operational efficiency, and drive innovation within the Ethiopian medical sector.

## Table of Contents

1. [Data Scraping and Collection Pipeline](#data-scraping-and-collection-pipeline)
2. [Data Cleaning and Transformation](#data-cleaning-and-transformation)
3. [Object Detection Using YOLO](#object-detection-using-yolo)
4. [Exposing the Collected Data Using FastAPI](#exposing-the-collected-data-using-fastapi)
5. [Postman Collection](#you-can-also-use-Postman-api-collection-found-in-below-link)
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

## DBT for Data Cleaning and Transformation

1. **Setting Up DBT**:

   ```sh
   pip install dbt
   dbt init dbt_med
   ```

### Data Cleaning

- Remove duplicates
- Handle missing values
- Standardize formats
- Validate data

### Data Cleaning Models DBT Doc

2. **Defining Models**:

   - Create DBT models (SQL files) for data transformation.
   - Run DBT models to load data into the data warehouse:
     ```sh
     dbt run
     ```

![dbt](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/dbt%20Docs_models.jpg)

### Storing Cleaned Data

- Store cleaned data in a database

### DBT Database(Warehouse) Doc

![dbt_db](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/dbt%20Docs_database.jpg)

### Fact table in Postgresql Database

![dbt_db](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/fact_table.png)

3. **Testing and Documentation**:
   ```sh
   dbt test
   dbt docs generate
   dbt docs serve
   ```

### DBT - Directed Acyclic Graph (DAG)

![dbt_dag](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/dbt-dag.png)

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

### Detection data in Postgresql database

![yolo](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/table_yolo_detection.png)

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

### FastAPI Swagger Documentation

![crud](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/fastapi_crud.png)

### Get All Telegram data

![get](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_telegram_data.png)
![get](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_telegram_data2.png)

### Get All Yolo detection results

![getyolo](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/assets/get_all_yolo_result.png)

## You can also use Postman api collection found in below link

[Postman collection link](https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse/blob/main/fastAPI/medicalAPI.postman_collection.json)

## Installation

Clone the repository and install the required packages:

```sh
git clone https://github.com/Daniel-Andarge/AiML-ethiopian-medical-biz-datawarehouse.git
cd AiML-ethiopian-medical-biz-datawarehouse
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

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
