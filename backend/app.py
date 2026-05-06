from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

_engines = {}


def get_engine(name):
    if name not in _engines:
        if name == 'cbf':
            from recommenders.content_based import ContentBasedEngine
            _engines['cbf'] = ContentBasedEngine()
        elif name == 'cf':
            from recommenders.collaborative import CollaborativeEngine
            _engines['cf'] = CollaborativeEngine()
        elif name == 'hybrid':
            from recommenders.hybrid import HybridEngine
            _engines['hybrid'] = HybridEngine()
        else:
            return None
    return _engines[name]


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'engines_loaded': list(_engines.keys())
    })


@app.route('/api/users', methods=['GET'])
def get_users():
    ratings = pd.read_csv('data/ratings.csv')
    user_ids = sorted(ratings['userId'].unique().tolist())
    return jsonify({
        'count': len(user_ids),
        'userIds': user_ids
    })


@app.route('/api/recommend/<string:engine>/<int:user_id>', methods=['GET'])
def recommend(engine, user_id):
    n = request.args.get('n', 10, type=int)

    eng = get_engine(engine)
    if eng is None:
        return jsonify({
            'error': f'Unknown engine "{engine}". Use cbf, cf, or hybrid.'
        }), 400

    results = eng.recommend(user_id=user_id, n=n)

    if not results:
        return jsonify({
            'error': f'No recommendations found for user {user_id}.'
        }), 404

    return jsonify({
        'userId': user_id,
        'engine': engine,
        'count': len(results),
        'recommendations': results
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Route not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)