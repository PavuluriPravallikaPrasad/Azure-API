# import os
# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# from flask_httpauth import HTTPTokenAuth
# from flask_sqlalchemy import SQLAlchemy

# # Initialize app and API
# app = Flask(__name__)
# api = Api(app)
# auth = HTTPTokenAuth(scheme='Bearer')

# # Secure API Key
# API_KEY = "40240292-dfda-445f-a065-3ccc25c0b8e7"

# # Set up the database URI from the environment variable
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# db = SQLAlchemy(app)

# # Dummy storage for received data (can be removed once the database is connected)
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

# # Define the User model (this will map to your database table)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100))
#     last_name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     username = db.Column(db.String(100), unique=True)
#     contact_number = db.Column(db.String(20))
#     address = db.Column(db.String(255))

#     def __init__(self, first_name, last_name, email, username, contact_number, address):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.username = username
#         self.contact_number = contact_number
#         self.address = address

# # POST method to store data in the database
# class UserResource(Resource):
#     @auth.login_required
#     def post(self):
#         data = request.get_json()

#         # Extract data from the request
#         first_name = data.get("first_name")
#         last_name = data.get("last_name")
#         email = data.get("email")
#         username = data.get("username")
#         contact_number = data.get("contact_number")
#         address = data.get("address")

#         # Create a new User record
#         new_user = User(first_name=first_name, last_name=last_name, email=email, 
#                         username=username, contact_number=contact_number, address=str(address))
        
#         try:
#             # Save the new user to the database
#             db.session.add(new_user)
#             db.session.commit()
#             return jsonify({"message": "Data saved successfully"})
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"message": f"Error saving data: {str(e)}"}), 500

# # GET method to retrieve all users from the database
# class GetUserResource(Resource):
#     @auth.login_required
#     def get(self):
#         try:
#             users = User.query.all()  # Get all users from the database
#             users_data = [{"first_name": user.first_name, "last_name": user.last_name, 
#                            "email": user.email, "username": user.username, 
#                            "contact_number": user.contact_number, "address": user.address} 
#                           for user in users]

#             return jsonify(users_data)
#         except Exception as e:
#             return jsonify({"message": f"Error retrieving data: {str(e)}"}), 500

# # Add resources to API
# api.add_resource(UserResource, '/user')
# api.add_resource(GetUserResource, '/users')

# # Run the app
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
#     app.run(host="0.0.0.0", port=port)

#####################################################################

import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# Initialize app and API
app = Flask(__name__)
api = Api(app)

# Secure API Key
API_KEY = "40240292-dfda-445f-a065-3ccc25c0b8e7"  # Your API Key

# Set up the database URI from the environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Dummy storage for received data (can be removed once the database is connected)
user_data = {}

# API key authentication
def verify_api_key():
    """Checks for the API Key in the query parameter"""
    key = request.args.get('api_key')  # Check the query parameter for API key
    if not key:
        key = request.headers.get('x-api-key')  # Also check if it's in headers (x-api-key)
    if key == API_KEY:
        return True
    return False

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
    address = db.Column(db.String(255))  # Store the address as a string

    def __init__(self, first_name, last_name, email, username, contact_number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.contact_number = contact_number
        self.address = address

# POST method to store data in the database
class UserResource(Resource):
    def post(self):
        # Check for API key
        if not verify_api_key():
            return jsonify({"message": "Unauthorized Access"}), 403

        try:
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

            # Save the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "Data saved successfully"})

        except Exception as e:
            # Catch all exceptions and return the error message for debugging
            db.session.rollback()  # Rollback any changes to avoid partial commits
            return jsonify({"message": f"Error saving data: {str(e)}"}), 500

# GET method to retrieve all users from the database
class GetUserResource(Resource):
    def get(self):
        # Check for API key
        if not verify_api_key():
            return jsonify({"message": "Unauthorized Access"}), 403

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

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)
