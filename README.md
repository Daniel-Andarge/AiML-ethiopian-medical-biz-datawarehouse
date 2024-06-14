# Ethiopian Medical Business Data Warehouse & Data Pipeline

The Ethiopian Medical Business Data Warehouse & Analytics Platform is a comprehensive data solution designed to empower the Ethiopian healthcare and medical industry. This project aims to build a robust and scalable data warehouse that consolidates data from various sources, including medical facilities, pharmaceutical companies, insurance providers, and government agencies. By leveraging advanced analytics and business intelligence techniques, the platform will provide data-driven insights to support decision-making, improve operational efficiency, and drive innovation within the Ethiopian medical sector.

## Table of Contents

1. [Task 1 - Data Scraping and Collection Pipeline](#task-1---data-scraping-and-collection-pipeline)
2. [Task 2 - Data Cleaning and Transformation](#task-2---data-cleaning-and-transformation)
3. [Task 3 - Object Detection Using YOLO](#task-3---object-detection-using-yolo)
4. [Task 4 - Exposing the Collected Data Using FastAPI](#task-4---exposing-the-collected-data-using-fastapi)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

## Task 1 - Data Scraping and Collection Pipeline

### Telegram Scraping

Utilize the Telegram API or custom scripts to extract data from public Telegram channels related to Ethiopian medical businesses. Key channels include:

- [DoctorsET](https://t.me/DoctorsET)
- [Chemed Telegram Channel](https://t.me/lobelia4cosmetics)
- [Yetenaweg](https://t.me/yetenaweg)
- [EAHCI](https://t.me/EAHCI)
- More channels from [tgstat](https://et.tgstat.com/medicine)

### Image Scraping

Collect images from specified Telegram channels for object detection:

- [Chemed Telegram Channel](https://t.me/lobelia4cosmetics)
- [Lobelia for Cosmetics](https://t.me/lobelia4cosmetics)

## Task 2 - Data Cleaning and Transformation

### Data Cleaning

- Remove duplicates
- Handle missing values
- Standardize formats
- Validate data

### Storing Cleaned Data

- Store cleaned data in a database

### DBT for Data Transformation

1. **Setting Up DBT**:

   ```sh
   pip install dbt
   dbt init my_project
   ```

2. **Defining Models**:

   - Create DBT models (SQL files) for data transformation.
   - Run DBT models to load data into the data warehouse:
     ```sh
     dbt run
     ```

3. **Testing and Documentation**:
   - Ensure data quality and provide context for transformations:
     ```sh
     dbt test
     dbt docs generate
     dbt docs serve
     ```

### Monitoring and Logging

- Implement logging to track the transformation process, capture errors, and monitor progress.

## Task 3 - Object Detection Using YOLO

### Setting Up the Environment

Ensure necessary dependencies are installed:

```sh
pip install opencv-python
pip install torch torchvision  # for PyTorch-based YOLO
pip install tensorflow  # for TensorFlow-based YOLO
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

### Monitoring and Logging

- Implement logging to track the object detection process, capture errors, and monitor progress.

## Task 4 - Exposing the Collected Data Using FastAPI

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
   python scrape_telegram.py
   ```

2. **Run DBT Models**:

   ```sh
   dbt run
   ```

3. **Run Object Detection**:

   ```sh
   python detect_objects.py
   ```

4. **Start FastAPI Application**:
   ```sh
   uvicorn main:app --reload
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
