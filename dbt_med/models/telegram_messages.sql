{{ config(
    materialized='table',
    schema='analysis',
    partition_by={
      "field": "timestamp",
      "data_type": "timestamp"
    },
    unique_key='id'
) }}

SELECT
  id,
  channel,
  message_id,
  content,
  timestamp,
  views,
  message_link
FROM
  public.telegram_messages
