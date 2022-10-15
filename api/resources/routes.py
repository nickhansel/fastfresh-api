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

