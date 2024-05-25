-- Le restaurant non-asiatique proposant le plus de plats qui sont généralement proposés dans des restaurant asiatiques
WITH AsianRestaurantDishes AS(
    SELECT rd.dish_id
    FROM Restaurants r
    JOIN RestaurantDishes rd ON r.restaurant_id = rd.restaurant_id
    WHERE r.cuisine_type = 'Asian'
),
