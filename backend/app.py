from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

# Item Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

def create_app():
    app = Flask(__name__)
    
    # Initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/items.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Routes
    @app.route('/')
    def home():
        return jsonify({'message': 'Flask CRUD API is running!'})
    
    # Get all items
    @app.route('/api/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items])
    
    # Get single item
    @app.route('/api/items/<int:item_id>', methods=['GET'])
    def get_item(item_id):
        item = Item.query.get_or_404(item_id)
        return jsonify(item.to_dict())
    
    # Create new item
    @app.route('/api/items', methods=['POST'])
    def create_item():
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        item = Item(
            name=data['name'],
            description=data.get('description', ''),
            price=data.get('price', 0.0)
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
    
    # Update item
    @app.route('/api/items/<int:item_id>', methods=['PUT'])
    def update_item(item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'name' in data:
            item.name = data['name']
        if 'description' in data:
            item.description = data['description']
        if 'price' in data:
            item.price = data['price']
        
        db.session.commit()
        return jsonify(item.to_dict())
    
    # Delete item
    @app.route('/api/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
