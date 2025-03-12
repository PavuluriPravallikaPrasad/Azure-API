# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# from flask_httpauth import HTTPTokenAuth
# import os

# app = Flask(__name__)  # Fix: __name__ instead of _name_
# api = Api(app)
# auth = HTTPTokenAuth(scheme='Bearer')

# # Secure API Key
# API_KEY = "your-secure-api-key"

# # Dummy storage for received data
# user_data = {}

# # API key authentication
# @auth.verify_token
# def verify_token(token):
#     """Allow Azure Health Checks Without API Key"""
#     if request.endpoint == "root":
#         return True  # Allow health check requests
#     return token == API_KEY

# # Home route (for health checks)
# @app.route('/')
# def root():
#     return jsonify({"message": "API is running!"})

# # POST method to store data
# class User(Resource):
#     @auth.login_required
#     def post(self):
#         data = request.get_json()
#         user_data.update(data)  # Store all received data
#         return {"message": "Data saved successfully"}, 201

# # GET method to retrieve data
# class GetUser(Resource):
#     @auth.login_required
#     def get(self):
#         return user_data, 200

# # Add resources to API
# api.add_resource(User, '/user')
# api.add_resource(GetUser, '/user/get')

# if __name__ == '__main__':  # Fix: __name__
#     port = int(os.environ.get("PORT", 8000))  # Use port 8000 for Azure
#     app.run(host="0.0.0.0", port=port)


from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
import os
import logging

# Initialize Flask App
app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

# Secure API Key (Set this as an environment variable in Azure)
API_KEY = os.getenv("API_SECRET_KEY", "your-secure-api-key")

# In-memory storage (can be replaced with a database)
user_data = {}

# Configure Logging
logging.basicConfig(level=logging.INFO)

# API key authentication
@auth.verify_token
def verify_token(token):
    """Allow only authorized requests using API Key."""
    return token == API_KEY

# Health Check Route
@app.route('/')
def root():
    return jsonify({"message": "API is running!"})

# POST method to store user data
class User(Resource):
    @auth.login_required
    def post(self):
        if not request.is_json:
            return jsonify({"error": "Invalid request, JSON expected"}), 400
        
        data = request.get_json()
        
        user_data["first_name"] = data.get("first_name", "")
        user_data["last_name"] = data.get("last_name", "")
        user_data["email"] = data.get("email", "")
        user_data["username"] = data.get("username", "")
        user_data["contact_number"] = data.get("contact_number", "")
        user_data["address"] = data.get("address", {})

        logging.info(f"User data received: {user_data}")
        return jsonify({"message": "User data stored successfully"}), 201

# GET method to retrieve stored user data
class GetUser(Resource):
    @auth.login_required
    def get(self):
        return jsonify(user_data), 200

# Register API Endpoints
api.add_resource(User, "/user")
api.add_resource(GetUser, "/user/get")

# Run Flask App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
