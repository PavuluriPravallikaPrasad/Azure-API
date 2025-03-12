# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# import os 

# app = Flask(__name__)
# api = Api(app)

# # Secure API Key
# API_KEY = "40240292-dfda-445f-a065-3ccc25c0b8e7"

# # Storage for multiple users
# users = []

# # Middleware for API Key Authentication
# def require_api_key(func):
#     def wrapper(*args, **kwargs):
#         api_key = request.headers.get("x-api-key")  # Get API key from headers
#         if not api_key or api_key != API_KEY:
#             return jsonify({"error": "Unauthorized access"}), 401
#         return func(*args, **kwargs)
#     return wrapper

# # Home route (for health checks)
# @app.route('/')
# def root():
#     return jsonify({"message": "API is running!"})

# # POST method to store user data
# class User(Resource):
#     @require_api_key
#     def post(self):
#         data = request.get_json()

#         if not data:
#             return jsonify({"error": "Invalid JSON payload"}), 400

#         user = {
#             "first_name": data.get("first_name"),
#             "last_name": data.get("last_name"),
#             "username": data.get("username"),
#             "email": data.get("email"),
#             "contact_number": data.get("contact_number"),
#             "address": data.get("address"),
#         }

#         users.append(user)  # Append user to the list

#         return jsonify({"message": "User data stored successfully"})

# # GET method to retrieve all users
# class GetUsers(Resource):
#     @require_api_key
#     def get(self):
#         return jsonify(users)  # Return list of all users

# # Add resources to API
# api.add_resource(User, "/user")
# api.add_resource(GetUsers, "/users")  # New endpoint for getting all users

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
#     app.run(host="0.0.0.0", port=port)

import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

# Initialize app and API
app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')

# Secure API Key
API_KEY = "40240292-dfda-445f-a065-3ccc25c0b8e7"

# Set up the database URI from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Dummy storage for received data (can be removed once the database is connected)
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

# Define the User model (this will map to your database table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(255))

    def __init__(self, first_name, last_name, email, username, contact_number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.contact_number = contact_number
        self.address = address

# POST method to store data in the database
class UserResource(Resource):
    @auth.login_required
    def post(self):
        data = request.get_json()

        # Extract data from the request
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        contact_number = data.get("contact_number")
        address = data.get("address")

        # Create a new User record
        new_user = User(first_name=first_name, last_name=last_name, email=email, 
                        username=username, contact_number=contact_number, address=str(address))
        
        try:
            # Save the new user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Data saved successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error saving data: {str(e)}"}), 500

# GET method to retrieve all users from the database
class GetUserResource(Resource):
    @auth.login_required
    def get(self):
        try:
            users = User.query.all()  # Get all users from the database
            users_data = [{"first_name": user.first_name, "last_name": user.last_name, 
                           "email": user.email, "username": user.username, 
                           "contact_number": user.contact_number, "address": user.address} 
                          for user in users]

            return jsonify(users_data)
        except Exception as e:
            return jsonify({"message": f"Error retrieving data: {str(e)}"}), 500

# Add resources to API
api.add_resource(UserResource, '/user')
api.add_resource(GetUserResource, '/users')

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)
