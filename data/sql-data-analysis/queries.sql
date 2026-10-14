-- Named query: account_summary
-- LEFT JOIN includes accounts with no activity; COUNT(e.id) avoids phantom rows.
SELECT u.username, COUNT(e.id) AS total_events,
       SUM(CASE WHEN e.outcome = 'failure' THEN 1 ELSE 0 END) AS failures
FROM users AS u LEFT JOIN login_events AS e ON e.user_id = u.id
GROUP BY u.id, u.username ORDER BY failures DESC, u.username;

-- Named query: repeated_failures
-- Threshold is a bound parameter. This is a whole-dataset count, not a time window.
SELECT source_ip, COUNT(*) AS failures
FROM login_events WHERE outcome = 'failure'
GROUP BY source_ip HAVING COUNT(*) >= :threshold
ORDER BY failures DESC, source_ip;
