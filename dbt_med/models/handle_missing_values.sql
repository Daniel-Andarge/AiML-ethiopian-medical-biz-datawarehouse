
WITH filled_content AS (
    SELECT
        id,
        channel,
        message_id,
        COALESCE(content, 'message not found') AS content,
        message_link,
        timestamp,
        views
    FROM {{ ref('remove_duplicates') }}
),

cleaned_data AS (
    SELECT
        *
    FROM filled_content
    WHERE channel IS NOT NULL
      AND message_id IS NOT NULL
      AND message_link IS NOT NULL
      AND timestamp IS NOT NULL
      AND views IS NOT NULL
)

SELECT
    *
FROM cleaned_data
