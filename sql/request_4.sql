-- Le restaurant non-asiatique proposant le plus de plats qui sont généralement proposés dans des restaurant asiatiques
-- Étape 1: Identifier les plats servis dans les restaurants asiatiques
WITH AsianRestaurantDishes AS (
    SELECT p.ID AS dish_id, p.NAME AS dish_name
    FROM restaurants r
    JOIN plats p ON r.MENU = p.MENU
    WHERE r.FOOD_TYPE = 'asiatique'
),

-- Étape 2: Compter combien de restaurants asiatiques servent chaque plat
DishCountInAsianRestaurants AS (
    SELECT dish_name, COUNT(*) AS asian_restaurant_count
    FROM AsianRestaurantDishes
    GROUP BY dish_name
),

-- Étape 3: Identifier les plats servis dans les restaurants non asiatiques
NonAsianRestaurantDishes AS (
    SELECT r.ID AS restaurant_id, p.NAME AS dish_name
    FROM restaurants r
    JOIN plats p ON r.MENU = p.MENU
    WHERE r.FOOD_TYPE != 'asiatique'
),

-- Étape 4: Compter le nombre de plats typiquement servis dans les restaurants asiatiques qui sont servis dans chaque restaurant non asiatique
PopularDishesInNonAsianRestaurants AS (
    SELECT nard.restaurant_id, COUNT(*) AS popular_dish_count
    FROM NonAsianRestaurantDishes nard
    JOIN DishCountInAsianRestaurants dar ON nard.dish_name = dar.dish_name
    WHERE dar.asian_restaurant_count >= 2
    GROUP BY nard.restaurant_id
)

-- Étape 5: Sélectionner le restaurant non asiatique avec le plus grand nombre de ces plats
SELECT r.NAME, r.FOOD_TYPE, pdr.popular_dish_count
FROM PopularDishesInNonAsianRestaurants pdr
JOIN restaurants r ON pdr.restaurant_id = r.ID
ORDER BY pdr.popular_dish_count DESC LIMIT 1;

