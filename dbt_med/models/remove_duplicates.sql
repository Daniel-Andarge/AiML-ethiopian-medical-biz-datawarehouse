
WITH ranked_messages AS (
    SELECT
        id,
        channel,
        message_id,
        content,
        message_link,
        timestamp,
        views,
        ROW_NUMBER() OVER (PARTITION BY message_id ORDER BY timestamp DESC) AS row_num
    FROM {{ ref('telegram_messages') }}
)

SELECT
    id,
    channel,
    message_id,
    content,
    message_link,
    timestamp,
    views
FROM ranked_messages
WHERE row_num = 1
