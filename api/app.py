from cgitb import reset
from json import load
import celery.states as states
from flask import Flask, Response
from flask import url_for, jsonify
from worker import celery
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_apispec import FlaskApiSpec
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

load_dotenv()

# run command: docker-compose -f docker-compose.yml -f docker-compose.development.yml up --build

dev_mode = True
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["APISPEC_SWAGGER_UI_URL"] = "/"
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

api = Api(app)
ma_ext = Marshmallow(app)

jwt_ext = JWTManager(app)

docs = FlaskApiSpec(app)

db_ext = SQLAlchemy(app)

limiter_ext = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute"]
)

from db import * 
from resources import *

# db_ext.create_all()

@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK health check")

@app.route('/test')
def test() -> Response:
    return jsonify("action works")

api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
