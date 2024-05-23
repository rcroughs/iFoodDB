-- Pour chaque tranche de score moyen (1/5, 2/5, 3/5, ...) de restaurant, le type de nourriture le plus représenté
WITH avg_scores AS ( -- Calcule al moyenne des notes de chaque restaurant
    SELECT
        id_restaurant,
        AVG(note) AS avg_score
    FROM
        notes
    GROUP BY
        id_restaurant
),
score_ranges AS ( -- Sépare les restaurants dans les tranches de notes associés
    SELECT
        id_restaurant,
        CASE
            WHEN avg_score >= 0 AND avg_score < 1 THEN 1
            WHEN avg_score >= 1 AND avg_score < 2 THEN 2
            WHEN avg_score >= 2 AND avg_score < 3 THEN 3
            WHEN avg_score >= 3 AND avg_score < 4 THEN 4
            WHEN avg_score >= 4 AND avg_score <= 5 THEN 5
        END AS score_range
    FROM
        avg_scores
),
restaurant_food_types AS ( -- Lie les restaurants à leur type de nourriture
    SELECT
        r.id AS restaurant_id,
        r.food_type AS type  
    FROM
        restaurants r
),
food_type_counts AS ( -- Compte le nombre d'occurence de chaque type de nourriture par catégorie de note
    SELECT
        sr.score_range,
        rt.type,
        COUNT(*) AS type_count
    FROM
        score_ranges sr
        JOIN restaurant_food_types rt ON sr.id_restaurant = rt.restaurant_id
    GROUP BY
        sr.score_range,
        rt.type
),
most_represented_type AS ( -- Récupère le type de nouritture le plus représenté par catégorie de note
    SELECT
        score_range,
        type,
        type_count,
        RANK() OVER (PARTITION BY score_range ORDER BY type_count DESC) AS rank
    FROM
        food_type_counts
)
SELECT
    score_range,
    type AS most_represented_type
FROM
    most_represented_type
WHERE
    rank = 1;
