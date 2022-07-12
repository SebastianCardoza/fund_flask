from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import burger

class Topping:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.on_burgers = []

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO toppings (name) VALUES (%(name)s)'
        return connectToMySQL('burgers').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM toppings;'
        results = connectToMySQL('burgers').query_db(query)
        toppings = []
        for topping in results:
            toppings.append(cls(topping))
        return toppings

    @classmethod
    def get_topping_with_burgers(cls, data):
        query = 'SELECT * FROM toppings LEFT JOIN add_ons ON toppings.id = add_ons.topping_id LEFT JOIN burgers ON burgers.id = add_ons.burger_id WHERE topping.id = %(id)s'
        results = connectToMySQL('burgers').query_db(query, data)
        topping = cls(results[0])
        for row_from_db in results:
            data1 = {
                'id':row_from_db['burgers.id'],
                'name':row_from_db['burgers.name'],
                'bun':row_from_db['bun'],
                'meat':row_from_db['meat'],
                'calories':row_from_db['calories'],
                'created_at':row_from_db['toppings.created_at'],
                'updated_at':row_from_db['toppings.updated_at']
            }
            topping.on_burgers.append(burger.Burger(data1))
        return topping 