from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
import os

app = Flask(_name_)
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
        
        user_data['first_name'] = data.get("first_name")
        user_data['last_name'] = data.get("last_name")
        user_data['username'] = data.get("username")
        user_data['email'] = data.get("email")
        user_data['contact_number'] = data.get("contact_number")
        user_data['address'] = data.get("address")

        return jsonify({"message": "Data saved successfully"})

# GET method to retrieve data
class GetUser(Resource):
    @auth.login_required
    def get(self):
        return jsonify(user_data)

# Add resources to API
api.add_resource(User, '/user')
api.add_resource(GetUser, '/user/get')

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)
