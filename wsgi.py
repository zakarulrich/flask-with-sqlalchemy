# pylint: disable=missing-docstring


from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Config
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

BASE_URL = '/api/v1'


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from schemas import many_product_schema, one_product_schema
from models import Product

migrate = Migrate(app, db)


@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    # SQLAlchemy request => 'SELECT * FROM products'
    products = db.session.query(Product).all()
    return many_product_schema.jsonify(products), 200


@app.route(f'{BASE_URL}/products/<id>', methods=['GET'])
def get_one_product(id):
    product = db.session.query(Product).get(int(id))
    return one_product_schema.jsonify(product), 200


@app.route(f'{BASE_URL}/products/<id>', methods=['PATCH'])
def update_product(id):
    data = request.get_json()
    if(id is None or data is None):
        abort(400)

    if(data.get('name') is None):
        abort(400)

    product = db.session.query(Product).get(int(id))
    if(product is None):
        abort(404)

    product.name = data.get('name')
    product.description = data.get('description')
    db.session.add(product)
    db.session.commit()
    return '', 200


@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if(data is None):
        abort(400)

    product = Product()
    product.name = data['name']
    product.description = data['description']
    db.session.add(product)
    db.session.commit()
    return one_product_schema.jsonify(product), 200


@app.route(f'{BASE_URL}/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.query(Product).get(int(id))
    if(product is None):
        abort(404)

    db.session.delete(product)
    db.session.commit()
    return '', 200


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200
