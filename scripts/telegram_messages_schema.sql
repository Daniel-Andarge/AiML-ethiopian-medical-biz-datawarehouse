
CREATE TABLE IF NOT EXISTS telegram_messages (
    id SERIAL PRIMARY KEY,
    channel TEXT,
    message_id INT,
    content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE,
    views FLOAT,
    message_link TEXT
);
