# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# from flask_httpauth import HTTPTokenAuth
# import os

# app = Flask(__name__)  # Fix: __name__ instead of _name_
# api = Api(app)
# auth = HTTPTokenAuth(scheme='Bearer')

# # Secure API Key
# API_KEY = "b9f1e4cb-894a-417c-8b35-764b277d7bda"

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
import os

app = Flask(__name__)
api = Api(app)

# Secure API Key
API_KEY = "your-secure-api-key"

# Storage for multiple users
users = []

# Middleware for API Key Authentication
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")  # Get API key from headers
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)
    return wrapper

# Home route (for health checks)
@app.route('/')
def root():
    return jsonify({"message": "API is running!"})

# POST method to store user data
class User(Resource):
    @require_api_key
    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        user = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "username": data.get("username"),
            "email": data.get("email"),
            "contact_number": data.get("contact_number"),
            "address": data.get("address"),
        }

        users.append(user)  # Append user to the list

        return jsonify({"message": "User data stored successfully"})

# GET method to retrieve all users
class GetUsers(Resource):
    @require_api_key
    def get(self):
        return jsonify(users)  # Return list of all users

# Add resources to API
api.add_resource(User, "/user")
api.add_resource(GetUsers, "/users")  # New endpoint for getting all users

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)

