# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# import os 

# app = Flask(__name__)
# api = Api(app)

# # Secure API Key
# API_KEY = "b9f1e4cb-894a-417c-8b35-764b277d7bda"

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

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)

# Secure API Key
API_KEY = "your-secure-api-key"

# Azure SQL Database Configuration
# Replace with your actual connection string
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 
    "mssql+pyodbc://<username>:<password>@<server>.database.windows.net:1433/<dbname>?driver=ODBC+Driver+17+for+SQL+Server")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model (maps to Users table in Azure SQL Database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(255))
    username = db.Column(db.String(100))
    contact_number = db.Column(db.String(50))
    address = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# Middleware for API Key Authentication
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")  # Get API key from headers
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)
    return wrapper

# POST method to store user data
class UserResource(Resource):
    @require_api_key
    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Create new user record
        new_user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            username=data.get("username"),
            contact_number=data.get("contact_number"),
            address=str(data.get("address"))
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User data stored successfully"}), 201

# GET method to retrieve all users
class GetUsers(Resource):
    @require_api_key
    def get(self):
        users = User.query.all()  # Query all users from the database
        users_list = [{"id": user.id, "first_name": user.first_name, "last_name": user.last_name,
                       "email": user.email, "username": user.username, "contact_number": user.contact_number,
                       "address": user.address} for user in users]
        return jsonify(users_list)

# Add resources to API
api.add_resource(UserResource, "/user")
api.add_resource(GetUsers, "/users")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)
