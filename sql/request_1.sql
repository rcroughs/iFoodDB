-- Les restaurants ayant un avis moyen de plus de 3
SELECT r.name, AVG(c.rating) AS average_rating
FROM Restaurant r
JOIN Comment c ON r.id = c.restaurant_id
GROUP BY r.name
HAVING AVG(c.rating) >= 3;