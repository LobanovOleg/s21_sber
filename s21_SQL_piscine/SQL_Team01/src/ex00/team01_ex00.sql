SELECT
    COALESCE(u.name, 'not defined') AS name,
    COALESCE(u.lastname, 'not defined') AS lastname,
    t1.type,
    t1.volume,
    COALESCE(c.name, 'not defined') AS currency_name,
    COALESCE((SELECT rate_to_usd
              FROM currency c1
              WHERE c1.id = c.id AND c1.updated = c.last_updated), 1) AS last_rate_to_usd,
    t1.volume::numeric * COALESCE((SELECT rate_to_usd
                                   FROM currency c1
                                   WHERE c1.id = c.id AND c1.updated = c.last_updated), 1) AS total_volume_in_usd
FROM (SELECT user_id, type, currency_id, SUM(money) AS volume
      FROM balance b
      GROUP BY user_id, type, currency_id) AS t1
FULL JOIN "user" u on u.id = t1.user_id
FULL JOIN (SELECT id, name, max(updated) AS last_updated
           FROM currency c
           GROUP BY id, name) AS c ON c.id = t1.currency_id
ORDER BY 1 DESC, 2, 3

