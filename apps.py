from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Ініціалізація додатку
app = Flask(__name__)
CORS(app)
api = Api(app)

# Налаштування підключення до бази даних PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<lunanya>:<Aboba8642>@<database-1.cj2aii6y8tqe.eu-north-1.rds.amazonaws.com>:5432/<database-1>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# ORM-модель для таблиці
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, index=True)  # Додаємо індекс
    price = db.Column(db.Float, nullable=False)

    def json(self):
        return {"id": self.id, "name": self.name, "price": self.price}

# Створення таблиці, якщо її немає
with app.app_context():
    db.create_all()

# API-ресурс для роботи з елементами
class Item(Resource):
    def get(self, name):
        item = ItemModel.query.filter_by(name=name).first()
        if item:
            return item.json(), 200
        return {"message": "Item not found"}, 404

    def post(self, name):
        data = request.get_json()
        if ItemModel.query.filter_by(name=name).first():
            return {"message": "Item already exists"}, 400
        new_item = ItemModel(name=name, price=data['price'])
        db.session.add(new_item)
        db.session.commit()
        return new_item.json(), 201

    def put(self, name):
        data = request.get_json()
        item = ItemModel.query.filter_by(name=name).first()
        if item:
            item.price = data['price']
            db.session.commit()
            return item.json(), 200
        new_item = ItemModel(name=name, price=data['price'])
        db.session.add(new_item)
        db.session.commit()
        return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.query.filter_by(name=name).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}, 200
        return {"message": "Item not found"}, 404

# Додаємо ресурс до API
api.add_resource(Item, '/item/<string:name>')

# Запуск додатку
if __name__ == '__main__':
    app.run(debug=True)
