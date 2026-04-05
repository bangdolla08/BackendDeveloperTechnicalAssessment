import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


def load_customers():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'data', 'customers.json')

    with open(file_path, 'r') as file:
        return json.load(file)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Paginated list of customers """
    all_customers = load_customers()

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start = (page - 1) * limit
    end = start + limit
    paginated_data = all_customers[start:end]

    return jsonify({
        "data": paginated_data,
        "total": len(all_customers),
        "page": page,
        "limit": limit
    }), 200


@app.route('/api/customers/<id>', methods=['GET'])
def get_customer_by_id(id):
    """Single customer by ID """
    all_customers = load_customers()

    customer = next((c for c in all_customers if c['customer_id'] == id), None)

    if customer:
        return jsonify(customer), 200

    return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)