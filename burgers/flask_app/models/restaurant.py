from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.burger import Burger

class Restaurant:
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # Creamos una lista para que luego podamos agregar todas las hamburguesas que están asociadas a un restaurante
        self.burgers = []
    @classmethod
    def save( cls , data ):
        query = "INSERT INTO restaurants ( name , created_at , updated_at ) VALUES (%(name)s,NOW(),NOW());"
        return connectToMySQL('burgers').query_db( query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM restaurants;'
        results = connectToMySQL('burgers').query_db(query=query)
        restaurants = []
        for restaurant in results :
            restaurants.append(cls(restaurant))
        return restaurants

    @classmethod
    def get_restaurant_with_burgers(cls, data):
        query = "SELECT * FROM restaurants LEFT JOIN burgers ON restaurants.id = burgers.restaurant_id WHERE id = %(id)s;"
        results = connectToMySQL('burgers').query_db(query, data)
        restaurant = cls(results[0])
        for row_from_db in results:
            burger_data = {
                "id": row_from_db["burgers.id"],
                "name": row_from_db["burgers.name"],
                "bun": row_from_db["burgers.bun"],
                "meat": row_from_db["burgers.meat"],
                "calories": row_from_db["burgers.calories"],
                "created_at": row_from_db["burgers.created_at"],
                "updated_at": row_from_db["burgers.updated_at"]
            }
            restaurant.burgers.append(Burger(burger_data))
        return restaurant