
SELECT
    id,
    channel,
    message_id,
    REGEXP_REPLACE(LOWER(content), '[^\w\s]', '') AS content,
    TIMESTAMP WITH TIME ZONE 'timestamp' AS timestamp,
    message_link,
    views
FROM {{ ref('handle_missing_values') }}
