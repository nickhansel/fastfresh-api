from db import *
from app import ma_ext as ma
from app import client
from marshmallow import Schema, fields
from flask_restful import reqparse, abort, Api, Resource
from flask_apispec import use_kwargs, marshal_with, MethodResource, doc
from flask import request, jsonify
from datetime import datetime, timedelta
import jwt
from  werkzeug.security import generate_password_hash, check_password_hash
import json
from app import limiter_ext
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

def get_data(data):
    data["_id"] = str(data["_id"])
    return data


class UserResource(MethodResource):
    @doc(description="Get a user")
    def get(self):
        # token = request.headers.get('Authorization')
        # token = token[7:]
        # data = jwt.decode(token, 'secret', algorithms=["HS256"])
        # user_id = data['sub']
        found = client.mydb.dogs.find({"id": 1})
        if not found: 
            return abort(400, message="User not found")
        else:
            j = [get_data(i) for i in found]
            return jsonify(j)

class ItemResource(MethodResource):
    def get(self):
        found = client.mydb.items.find()
        if not found: 
            return abort(400, message="User not found")
        else:
            j = [get_data(i) for i in found]
            return jsonify(j)

    @doc(description="Get an item")
    def post(self):
        name = request.json.get('name')
        quantity = request.json.get('quantity')
        price = request.json.get('price')
        url = request.json.get('url')
        type = request.json.get('type')
        id = request.json.get('id')
        if not name or not quantity or not price or not url or not type or not id:
            return abort(400, message="Missing data")
        else:
            client.mydb.items.insert_one({"name": name, "quantity": quantity, "price": price, "url": url, "type": type, "id": id})
            return jsonify({"message": "Item added"})

class SellerResource(MethodResource):
    def get(self):
        found = client.mydb.sellers.find()
        if not found: 
            return abort(400, message="User not found")
        else:
            j = [get_data(i) for i in found]
            return jsonify(j)

    @doc(description="Get a seller")
    def post(self):
        name = request.json.get('name')
        id = request.json.get('id')
        address = request.json.get('address')
        categories = request.json.get('categories')
        fee = request.json.get('fee')
        items = request.json.get('items')
        url = request.json.get('url')

        if not name or not id or not address or not categories or not fee or not items:
            return abort(400, message="Missing data")
        else:
            client.mydb.sellers.insert_one({"name": name, "id": id, "address": address, "categories": categories, "fee": fee, "items": items})
            return jsonify({"message": "Seller added"})

