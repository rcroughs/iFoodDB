-- Le restaurant avec le plat le plus cher
WITH most_expensive_dish AS ( -- Récupère le plat le plus cher par restaurant
    SELECT 
        r.name AS NomRestaurant,
        p.name AS NomPlat,
        p.price
    FROM
        restaurants r,
        plats p
    WHERE
        p.menu = r.menu 
    AND 
        p.price = (SELECT MAX(price) FROM plats p WHERE p.menu = r.menu )
)
SELECT -- Récupère le plat le plus cher entre tous les restaurants
    med.NomRestaurant,
    med.NomPlat,
    med.price
FROM 
    most_expensive_dish med
WHERE 
    med.price = (SELECT MAX(med.price) FROM most_expensive_dish med);