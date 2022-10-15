from app import ma_ext as ma
from app import db_ext as db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    
    email= db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    orders = db.relationship('orders', backref='users', lazy=True, uselist=True)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), nullable=False)
    order_id = db.relationship(db.Integer, db.ForeignKey('orders.id'), lazy=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(100), unique=False, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.relationship(db.Integer, db.ForeignKey('users.id'), lazy=True)
    total_price = db.Column(db.Integer, nullable=False)
    driver = db.relationship(db.Integer, db.ForeignKey('drivers.id'), lazy=True)
    seller = db.relationship(db.Integer, db.ForeignKey('sellers.id'), lazy=True)
    created_at =  db.Column(db.DateTime, nullable=False)
    delivered_at = db.Column(db.DateTime, nullable=True)
    item = db.relationship(db.Integer, db.ForeignKey('items.id'), lazy=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    seller_fee = db.relationship(db.Integer, db.ForeignKey('sellers.id'), lazy=True)

class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    driver = db.relationship(db.Integer, db.ForeignKey('drivers.id'), lazy=True)
    completed_sales = db.relationship(db.Integer, db.ForeignKey('orders.id'), lazy=True)
    stock = db.relationship(db.Integer, db.ForeignKey('items.id'), lazy=True)
    fee = db.Column(db.Integer, nullable=False)
    categories = db.Column(db.ARRAY(db.String(50)), nullable=False)
    

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    completed_orders = db.relationship(db.Integer, db.ForeignKey('orders.id'), lazy=True)



# fee
# categories - list

