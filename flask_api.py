from flask import Flask, jsonify, request
import pandas as pd
import ast
import random
from datetime import datetime

app = Flask(__name__)

# Load data
def load_data():
    df = pd.read_csv('places.csv')
    # Convert coordinates string to list
    df['coordinates'] = df['coordinates'].apply(ast.literal_eval)
    return df

# Secret travel tips
SECRET_TIPS = [
    "🔐 Ghumakkad's Secret Tip: If you're visiting a temple early morning, carry a small packet of sweets—some locals say it brings you unexpected blessings! 😉🍬",
    "🔐 Ghumakkad's Secret Tip: Always carry a small mirror when visiting forts—locals believe it helps ward off negative energy! ✨🪞",
    "🔐 Ghumakkad's Secret Tip: Visit lakes during sunrise with a cup of chai—the combination of mist and morning light creates magical moments! ☕🌅",
    "🔐 Ghumakkad's Secret Tip: For scary roads, play local folk music in your car—it's said to keep spirits at bay! 🎵👻",
    "🔐 Ghumakkad's Secret Tip: Carry a small bell when trekking—the sound helps you stay connected with your group in dense forests! 🔔🌲",
    "🔐 Ghumakkad's Secret Tip: Visit gardens on weekdays for the most peaceful experience—weekends can get crowded! 🌸📅",
    "🔐 Ghumakkad's Secret Tip: For mysterious places, visit during full moon—the atmosphere becomes even more enchanting! 🌕✨",
    "🔐 Ghumakkad's Secret Tip: Always greet the local deity before starting your journey—it's considered auspicious! 🙏🕉️"
]

@app.route('/')
def home():
    """Home page with API information"""
    return jsonify({
        'success': True,
        'message': '🗓️ Pune Weekend Diaries API',
        'description': 'Welcome to the Pune Weekend Diaries API! Use these endpoints to get travel data.',
        'endpoints': {
            'GET /api/places': 'Get all places',
            'GET /api/places?category=Nature&max_distance=50&spooky=false': 'Get filtered places with query parameters',
            'GET /api/places/random': 'Get a random place',
            'GET /api/tips': 'Get a random secret travel tip',
            'GET /api/categories': 'Get all available categories',
            'GET /api/stats': 'Get statistics about the places',
            'GET /api/places/<id>': 'Get a specific place by ID'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/places')
def get_places():
    """Get all places with optional filtering"""
    try:
        df = load_data()
        
        # Get query parameters
        category = request.args.get('category')
        max_distance = request.args.get('max_distance', type=float)
        spooky = request.args.get('spooky', type=str)
        
        # Apply filters
        if category:
            df = df[df['category'] == category]
        
        if max_distance:
            df = df[df['distance_from_pune_km'] <= max_distance]
        
        if spooky is not None:
            if spooky.lower() == 'true':
                df = df[df['spooky'] == True]
            elif spooky.lower() == 'false':
                df = df[df['spooky'] == False]
        
        # Convert to JSON
        places = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'count': len(places),
            'places': places,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/places/random')
def get_random_place():
    """Get a random place"""
    try:
        df = load_data()
        random_place = df.sample(n=1).iloc[0].to_dict()
        
        return jsonify({
            'success': True,
            'place': random_place,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/tips')
def get_random_tip():
    """Get a random secret travel tip"""
    try:
        tip = random.choice(SECRET_TIPS)
        
        return jsonify({
            'success': True,
            'tip': tip,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/categories')
def get_categories():
    """Get all available categories"""
    try:
        df = load_data()
        categories = sorted(df['category'].unique().tolist())
        
        return jsonify({
            'success': True,
            'categories': categories,
            'count': len(categories),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get statistics about the places"""
    try:
        df = load_data()
        
        stats = {
            'total_places': len(df),
            'categories': df['category'].value_counts().to_dict(),
            'spooky_places': int(df['spooky'].sum()),
            'non_spooky_places': int((~df['spooky']).sum()),
            'avg_distance': float(df['distance_from_pune_km'].mean()),
            'max_distance': float(df['distance_from_pune_km'].max()),
            'min_distance': float(df['distance_from_pune_km'].min()),
            'best_times': df['best_time_to_visit'].value_counts().to_dict()
        }
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/places/<int:place_id>')
def get_place_by_id(place_id):
    """Get a specific place by ID"""
    try:
        df = load_data()
        place = df[df['id'] == place_id]
        
        if place.empty:
            return jsonify({
                'success': False,
                'error': f'Place with ID {place_id} not found',
                'timestamp': datetime.now().isoformat()
            }), 404
        
        place_data = place.iloc[0].to_dict()
        
        return jsonify({
            'success': True,
            'place': place_data,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    print("🗓️ Starting Pune Weekend Diaries API...")
    print("📖 Available endpoints:")
    print("   - GET / (Home page)")
    print("   - GET /api/places (All places)")
    print("   - GET /api/places/random (Random place)")
    print("   - GET /api/tips (Random tip)")
    print("   - GET /api/categories (All categories)")
    print("   - GET /api/stats (Statistics)")
    print("   - GET /api/places/<id> (Specific place)")
    print("\n🚀 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 