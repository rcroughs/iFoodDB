-- Les 10 clients ayant consommé le plus de mexicains
WITH mexican_consumption AS ( -- Récupère le nombre de fois que chaque client à mangé mexicain
    SELECT
        n.id_client,
        COUNT(*) AS mexican_count
    FROM
        notes n
        JOIN restaurants r ON n.id_restaurant = r.id
    WHERE
        r.food_type = 'mexicain'
    GROUP BY
        n.id_client
)
SELECT -- Selectionne les 10 client qui ont mang le plus de mexicain
    u.id AS user_id,
    u.name AS user_name,
    mc.mexican_count
FROM
    mexican_consumption mc
    JOIN users u ON mc.id_client = u.id
ORDER BY
    mc.mexican_count DESC
LIMIT
    10;
