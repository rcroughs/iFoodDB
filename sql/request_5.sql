-- Le code postal de la ville dans laquelle les restaurants sont les moins bien notés en moyenne
WITH average_per_restaurant AS ( -- Calcule la note moyenne de chaque restaurant
    SELECT
        r.name as NomRestaurant,
        r.zip_code as CodePostal,
        AVG(n.note) as MoyenneNote
    FROM 
        restaurants r
        JOIN Notes n ON r.id = n.id_restaurant    
    GROUP BY
        r.name,
        r.zip_code 
),
average_per_city AS ( -- Calcule la note moyenne des restaurants pour chaque ville
    SELECT
        CodePostal,
        AVG(MoyenneNote) as MoyenneParVille
    FROM
        average_per_restaurant   
    GROUP BY
        CodePostal        
)
SELECT -- Finalement, sélectionne la note la plus basse dans ce classement
    CodePostal,
    MoyenneParVille
FROM
    average_per_city
WHERE 
    MoyenneParVille = (SELECT MIN(MoyenneParVille) FROM average_per_city);

