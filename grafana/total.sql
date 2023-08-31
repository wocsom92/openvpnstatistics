SELECT strftime('%s', formatted_date) AS time,
       SUM(bytes_sent) AS total_bytes
FROM (
  SELECT strftime('%Y-%m-%d', db_updated) AS formatted_date,
         bytes_sent
  FROM connections
  WHERE db_updated >= datetime('now', '-30 day')
) subquery
GROUP BY formatted_date
ORDER BY formatted_date;