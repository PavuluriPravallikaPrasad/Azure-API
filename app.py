from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
import os

app = Flask(__name__)  # Fix: __name__ instead of _name_
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

# Secure API Key
API_KEY = "your-secure-api-key"

# Dummy storage for received data
user_data = {}

# API key authentication
@auth.verify_token
def verify_token(token):
    """Allow Azure Health Checks Without API Key"""
    if request.endpoint == "root":
        return True  # Allow health check requests
    return token == API_KEY

# Home route (for health checks)
@app.route('/')
def root():
    return jsonify({"message": "API is running!"})

# POST method to store data
class User(Resource):
    @auth.login_required
    def post(self):
        data = request.get_json()
        user_data.update(data)  # Store all received data
        return {"message": "Data saved successfully"}, 201

# GET method to retrieve data
class GetUser(Resource):
    @auth.login_required
    def get(self):
        return user_data, 200

# Add resources to API
api.add_resource(User, '/user')
api.add_resource(GetUser, '/user/get')

if __name__ == '__main__':  # Fix: __name__
    port = int(os.environ.get("PORT", 8000))  # Use port 8000 for Azure
    app.run(host="0.0.0.0", port=port)
