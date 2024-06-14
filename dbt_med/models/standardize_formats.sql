
SELECT
  id,
  COALESCE(channel, 'unknown') AS channel,
  COALESCE(message_id, 0) AS message_id,
  TRIM(LOWER(REGEXP_REPLACE(COALESCE(content, 'n/a'), '[^\w\s]', ''))) AS content,
  COALESCE(CAST(timestamp AS TIMESTAMP), CURRENT_TIMESTAMP) AS timestamp,
  COALESCE(message_link, 'n/a') AS message_link,
  COALESCE(views, 0) AS views
FROM
  {{ ref('handle_missing_values') }}