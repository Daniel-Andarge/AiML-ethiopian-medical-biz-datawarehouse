
{{ config(
    materialized='test'
) }}

WITH source_data AS (
  SELECT
    id,
    channel,
    message_id,
    content,
    timestamp,
    views,
    message_link,
    message_length
  FROM {{ ref('fact_telegram') }}
),

validation_checks AS (
  SELECT
    id,
    channel,
    message_id,
    content,
    timestamp,
    views,
    message_link,
    message_length,
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(content, '!', ''), '@', ''), '#', ''), '$', ''), '%', ''), '^', '') AS cleaned_content,
    LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(content, '!', ''), '@', ''), '#', ''), '$', ''), '%', ''), '^', '')) AS lowercased_content
  FROM source_data
)

SELECT
  *
FROM validation_checks
WHERE
  -- Check for emojis or unexpected characters in content column
  cleaned_content <> content
  -- Check for lowercase content
  OR lowercased_content <> content
  -- Check for unique row IDs
  OR id IN (
    SELECT id
    FROM validation_checks
    GROUP BY id
    HAVING COUNT(*) > 1
  )
  -- Check for NULL values
  OR id IS NULL
  OR channel IS NULL
  OR message_id IS NULL
  OR content IS NULL
  OR timestamp IS NULL
  OR views IS NULL
  OR message_link IS NULL
  OR message_length IS NULL
