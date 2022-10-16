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

# user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     items = db.relationship('Item', backref='orders', lazy=True, uselist=True)
#     total_price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     driver = db.Column(db.String(50), nullable=True)
#     seller_feedback = db.Column(db.Float, nullable=True)
#     delivered_at = db.Column(db.DateTime, nullable=True)
#     created_at = db.Column(db.DateTime, nullable=False)
#     seller = db.relationship('Seller', backref='orders', lazy=True, uselist=False)


class OrderResource(MethodResource):
    def get(self):
        found = client.mydb.orders.find()
        if not found: 
            return abort(400, message="Order not found")
        else:
            j = [get_data(i) for i in found]
            return jsonify(j)

    @doc(description="Get a Order")
    def post(self):
        user_id = request.json.get('user_id')
        total_price = request.json.get('total_price')
        items = request.json.get('items')
        id = request.json.get('id')
        status = request.json.get('status')
        driver = request.json.get('driver')
        created_at = request.json.get('created_at')
        delivered_at = request.json.get('delivered_at')
        seller = request.json.get('seller')
        address = request.json.get('address')

        if not user_id or not total_price or not id or not status or not driver or not created_at or not delivered_at or not seller or not address:
            return abort(400, message="Missing data")
        else:
            client.mydb.orders.insert_one({"user_id": user_id, "address": address,"total_price": total_price, "id": id, "status": status, "items": items, "driver": driver,  "created_at": created_at, "delivered_at": delivered_at, "seller": seller})
            return jsonify({"message": "Order Added"})