# Databricks notebook source
# MAGIC %pip install Flask flask-restful flask-httpauth

# COMMAND ----------

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

# Sample API key for demonstration. In a real-world scenario, this would be stored securely.
API_KEY = "your-secure-api-key"

# Dummy storage for received data 1
user_data = {}

# API key authentication
@auth.verify_token
def verify_token(token):
    if token == API_KEY:
        return True
    return False

# POST method to store data
class User(Resource):
    def post(self):
        data = request.get_json()
        
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        contact_number = data.get("contact_number")
        address = data.get("address")
        
        # Save data to the dummy storage (for demonstration purposes)
        user_data['first_name'] = first_name
        user_data['last_name'] = last_name
        user_data['username'] = username
        user_data['email'] = email
        user_data['contact_number'] = contact_number
        user_data['address'] = address
        
        return jsonify({"message": "Data saved successfully"})

# GET method to retrieve data
class GetUser(Resource):
    def get(self):
        return jsonify(user_data)

# Add resources to API
api.add_resource(User, '/user')
api.add_resource(GetUser, '/user/get')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
