from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProductType(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    coefficient = db.Column(db.Numeric(5, 2), default=1.0, nullable=False)
    
    products = db.relationship('Product', backref='product_type', lazy=True)

class MaterialType(db.Model):
    __tablename__ = 'material_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    waste_percentage = db.Column(db.Numeric(5, 2), default=0.0, nullable=False)
    
    products = db.relationship('Product', backref='main_material', lazy=True)

class Workshop(db.Model):
    __tablename__ = 'workshops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    worker_count = db.Column(db.Integer, default=0, nullable=False)
    
    product_workshops = db.relationship('ProductWorkshop', backref='workshop', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(50), unique=True, nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    min_cost_for_partner = db.Column(db.Numeric(10, 2), nullable=False)
    main_material_id = db.Column(db.Integer, db.ForeignKey('material_types.id'), nullable=True)
    parameter1 = db.Column(db.Numeric(10, 2), default=0.0)
    parameter2 = db.Column(db.Numeric(10, 2), default=0.0)
    production_time = db.Column(db.Numeric(10, 2), default=0.0)
    
    product_workshops = db.relationship('ProductWorkshop', backref='product', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProductWorkshop(db.Model):
    __tablename__ = 'product_workshops'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshops.id'), nullable=False)
    time_in_workshop = db.Column(db.Numeric(10, 2), default=0.0, nullable=False)
    worker_count = db.Column(db.Integer, default=1, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('product_id', 'workshop_id', name='uq_product_workshop'),)