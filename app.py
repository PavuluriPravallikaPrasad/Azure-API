from flask import Flask, jsonify, request
import os

app = Flask(_name_)

# Secure API Key #
API_KEY = "mysecureapikey123"

# Sample data store
data_store = [
    {
        "firstname": "Likhitha",
        "lastname": "Aaraga",
        "email": "likhitha@gmail.com",
        "username": "likhitha123",
        "address": {
            "street": "123 Main St",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500081"
        },
        "contact_number": "9876543210"
    },
    {
        "firstname": "Pravallika",
        "lastname": "Pavuluri",
        "email": "pravallika@gmail.com",
        "username": "pravallika456",
        "address": {
            "street": "456 Park Ave",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560001"
        },
        "contact_number": "8765432109"
    }
]

# Middleware to check API Key
@app.before_request
def require_api_key():
    """Check if API Key is valid."""
    if request.endpoint != "home":  # Allow home route without authentication
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized - Invalid API Key"}), 403

# Home route (No API key required)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

if _name_ == '_main_':
    port = int(os.environ.get("PORT", 8080))  # Use Azure's dynamic port
    app.run(host="0.0.0.0", port=port)
