# pylint: disable=missing-docstring

from wsgi import ma
from models import Product


class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name')


one_product_schema = ProductSchema()
many_product_schema = ProductSchema(many=True)
