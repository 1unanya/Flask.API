from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS  # Імпортуємо CORS

app = Flask(__name__)
CORS(app)  # Додаємо підтримку CORS
api = Api(app)

items = {}  # Словник для зберігання елементів

class Item(Resource):
    def get(self, name):
        item = items.get(name)
        if item:
            return item, 200
        return {"message": "Item not found"}, 404

    def post(self, name):
        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items[name] = item
        return item, 201

    def put(self, name):
        data = request.get_json()
        if name in items:
            item = {"name": name, "price": data["price"]}
            items[name] = item
            return item, 200
        return {"message": "Item not found"}, 404

    def delete(self, name):
        if name in items:
            del items[name]
            return {"message": "Item deleted"}, 200
        return {"message": "Item not found"}, 404

# Додаємо ресурс до API
api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
