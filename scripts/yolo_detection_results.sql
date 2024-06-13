CREATE TABLE IF NOT EXISTS yolo_detection_results (
    id SERIAL PRIMARY KEY,
    class_label INTEGER,
    x_center FLOAT,
    y_center FLOAT,
    width FLOAT,
    height FLOAT,
    confidence FLOAT
);
