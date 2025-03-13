#####################################################################
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
#####################################################################
#----------------Blob
# import os
# import json
# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# from azure.storage.blob import BlobServiceClient, ContainerClient

# # Initialize app and API
# app = Flask(__name__)
# api = Api(app)

# # Secure API Key (you can store it in environment variables for better security)
# API_KEY = os.getenv("API_KEY")  # Retrieve API Key from environment variable

# # Set up the Azure Blob Storage connection string
# STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# # Initialize the Blob Service Client
# blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

# # Define the container name for storing user data
# container_name = "api-test"

# # Ensure the container exists (if not, create it)
# try:
#     # Get container client and create the container if it doesn't exist
#     container_client = blob_service_client.get_container_client(container_name)
#     container_client.create_container()  # Will raise an error if container already exists
#     print(f"Container {container_name} created successfully.")
# except Exception as e:
#     # Handle the case where the container already exists or another error occurred
#     print(f"Container creation failed or container already exists: {str(e)}")
#     container_client = blob_service_client.get_container_client(container_name)

# # Function to check API key from the request headers
# def check_api_key():
#     """Check if the API Key is correct"""
#     api_key_from_header = request.headers.get('X-API-KEY')  # Custom header for API key
#     if api_key_from_header == API_KEY:
#         return True
#     return False

# # Home route (for health checks)
# @app.route('/')
# def root():
#     return jsonify({"message": "API is running!"})

# # POST method to store user data in Azure Blob Storage
# class UserResource(Resource):
#     def post(self):
#         # Check if API Key is valid
#         if not check_api_key():
#             return jsonify({"message": "Unauthorized Access"}), 401
        
#         data = request.get_json()

#         # Extract data from the request
#         first_name = data.get("first_name")
#         last_name = data.get("last_name")
#         email = data.get("email")
#         username = data.get("username")
#         contact_number = data.get("contact_number")
#         address = data.get("address")

#         # Prepare the user data (can be converted to JSON format)
#         user_data = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": email,
#             "username": username,
#             "contact_number": contact_number,
#             "address": address
#         }

#         # Upload the data to Azure Blob Storage
#         try:
#             blob_name = f"{username}.json"  # Use username as the blob name
#             blob_client = container_client.get_blob_client(blob_name)

#             # Convert user data to JSON and upload it to Blob Storage
#             blob_client.upload_blob(json.dumps(user_data), overwrite=True)

#             return jsonify({"message": "User data saved successfully"})
#         except Exception as e:
#             return jsonify({"message": f"Error saving data: {str(e)}"}), 500

# # GET method to retrieve all user data from Azure Blob Storage
# class GetUserResource(Resource):
#     def get(self):
#         # Check if API Key is valid
#         if not check_api_key():
#             return jsonify({"message": "Unauthorized Access"}), 401
        
#         try:
#             # List all blobs in the container (retrieve all user files)
#             blob_list = container_client.list_blobs()

#             # Initialize an empty list to store user data
#             users_data = []

#             # Iterate over the blobs and retrieve user data
#             for blob in blob_list:
#                 blob_client = container_client.get_blob_client(blob)
#                 user_data = json.loads(blob_client.download_blob().readall())

#                 # Add user data to the list
#                 users_data.append(user_data)

#             return jsonify(users_data)
#         except Exception as e:
#             return jsonify({"message": f"Error retrieving data: {str(e)}"}), 500

# # Add resources to API
# api.add_resource(UserResource, '/user')  # POST method for storing data
# api.add_resource(GetUserResource, '/users')  # GET method for retrieving data

# # Run the app
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
#     app.run(host="0.0.0.0", port=port)
