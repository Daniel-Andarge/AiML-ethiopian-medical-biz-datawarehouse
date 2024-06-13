-- models/final_telegram.sql

{{ 
  config(
    materialized='incremental',
    schema='analysis',
    partition_by={
      "field": "timestamp",
      "data_type": "timestamp"
    },
    unique_key='id',
    incremental_strategy='merge'
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
  FROM {{ ref('telegram_messages') }}
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
