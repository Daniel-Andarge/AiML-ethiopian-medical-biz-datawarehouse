{{ 
  config(
    materialized='table',
    schema='analysis',
    partition_by={
      "field": "timestamp",
      "data_type": "timestamp"
    },
    unique_key='id'
  ) 
}}

WITH source_data AS (
  SELECT
    id,
    channel,
    message_id,
    content,
    timestamp,
    views,
    message_link,
    LENGTH(content) AS message_length
  FROM {{ ref('standardize_formats') }}
)

SELECT
  id,
  channel,
  message_id,
  content,
  timestamp,
  views,
  message_link,
  message_length
FROM source_data

{% if is_incremental() %}

-- Remove duplicates for incremental load
WHERE id NOT IN (
    SELECT id
    FROM {{ this }}
)

{% endif %}
