from app import ma_ext as ma
from app import db_ext as db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    
    email= db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    # get all orders where user_id = id
    orders = db.relationship('Order', backref='user', lazy=True, uselist=True)
    location = db.Column(db.String(50), nullable=False)
    is_driver = db.Column(db.Boolean, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('Item', backref='orders', lazy=True, uselist=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    driver = db.Column(db.String(50), nullable=True)
    seller_feedback = db.Column(db.Float, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    seller = db.relationship('Seller', backref='orders', lazy=True, uselist=False)

class ItemStock(db.Model):
    __tablename__ = 'item_stock'
    id = db.Column(db.Integer, primary_key=True)
    
    items = db.relationship('Item', backref='item_stock', lazy=True, uselist=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(50), nullable=False)
    # link to order all orders that have this item
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    # link to item_stock
    item_stock_id = db.Column(db.Integer, db.ForeignKey('item_stock.id'), nullable=False)

class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    orders = db.relationship('Order', backref='sellers', lazy=True, uselist=True)
    stock = db.relationship('Item', backref='sellers', lazy=True, uselist=True)
    categories = db.Column(db.ARRAY(db.String(50)), nullable=False)
