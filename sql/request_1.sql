-- Les restaurants ayant un avis moyen de plus de 3
SELECT r.name, AVG(c.note) AS average_rating
FROM restaurants r
JOIN notes c ON r.id = c.id_restaurant
GROUP BY r.name
HAVING AVG(c.note) >= 3;
