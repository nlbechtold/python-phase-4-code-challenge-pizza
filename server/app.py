#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class All_restaurants(Resource):
    def get(self):
        ar = Restaurant.query.all()
        r_l = []
        for restaurant in ar:
            r_l.append(restaurant.to_dict(rules=('-restaurant_pizzas',)))
        return r_l


class One_Restaurant(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
           
            return restaurant.to_dict(rules=('-restaurant_pizzas.pizza.restaurant_pizzas',))
        else:
            return {"error": "Restaurant not found"}, 404
    def delete(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id==id).first()
        if restaurant:
            restaurant_restaurant_pizzas = RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == id).all()
            for restaurant_pizza in restaurant_restaurant_pizzas:
                db.session.delete(restaurant_pizzas)
            db.session.delete(restaurant)
            db.session.commit()

            return {},204
        else:
            return {
                "error": "Restaurant not found"
            },404

class All_pizzas(Resource):
    def get(self):
        ap = Pizza.query.all()
        p_l = []
        for pizza in ap:
            p_l.append(pizza.to_dict(rules=('-pizza_restaurants',)))
        return p_l

class Restaurant_Pizza(Resource):
    def post(self):
        data = request.get_json()

        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')
        price = data.get('price')

        if not pizza_id or not restaurant_id or not price:
            return {"errors": ['validation errors']}, 400

        try:
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)

            if not pizza or not restaurant:
                return { "errors": ["validation errors"]}, 404

            restaurant_pizza = RestaurantPizza(
                pizza_id=pizza_id,
                restaurant_id=restaurant_id,
                price=price
            )
            db.session.add(restaurant_pizza)
            db.session.commit()

            return restaurant_pizza.to_dict(), 201

        except ValueError as e:
            
            return {"errors": ["validation errors"]}, 400
  

api.add_resource(All_restaurants,'/restaurants') 
api.add_resource(One_Restaurant,'/restaurants/<int:id>')    
api.add_resource(All_pizzas,'/pizzas')   
api.add_resource(Restaurant_Pizza,'/restaurant_pizzas')




if __name__ == "__main__":
    app.run(port=5555, debug=True)
