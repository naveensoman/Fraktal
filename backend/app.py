from flask import Flask, request, jsonify
from .database import init_db
from .models import db, User
# It's good practice to use a more secure way to hash passwords in a real app
# For example, from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure a default database URI.
# For local development, you might use SQLite: 'sqlite:///dev.db'
# For production, use your actual PostgreSQL URI, possibly from environment variables.
DATABASE_URI = 'sqlite:///./test.db' # Using a local SQLite file for simplicity

# Placeholder database interaction functions (modified to simulate ORM interaction)
def create_user(username, email, password):
    """
    Placeholder for creating a new user in the database.
    This function will be replaced with actual database logic.
    Simulates adding a user to the database and checking for existence.
    """
    # In a real app, password would be hashed here before storing
    # from werkzeug.security import generate_password_hash
    # password_hash = generate_password_hash(password)

    # Simulate checking if user or email already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        print(f"User {username} or email {email} already exists.")
        return None

    # Simulate creating and saving the new user object
    # new_user = User(username=username, email=email, password_hash=password_hash)
    # db.session.add(new_user)
    # db.session.commit()
    # print(f"User {username} created successfully with ID {new_user.user_id}.")
    # return {"user_id": new_user.user_id, "username": new_user.username, "email": new_user.email}

    # For now, returning a dictionary as placeholder functions did
    print(f"Simulating creation of user: {username}")
    # This part is still a placeholder, actual DB interaction is commented out
    if username == "existinguser": # Maintain previous placeholder behavior for now
        return None
    return {"user_id": 1, "username": username, "email": email, "password_hash": "simulated_hash_for_"+password}


def get_user_by_username(username):
    """
    Placeholder for fetching a user by username from the database.
    This function will be replaced with actual database logic.
    Simulates querying the database for a user.
    """
    # Simulate querying the database
    # user = User.query.filter_by(username=username).first()
    # if user:
    #     return {"user_id": user.user_id, "username": user.username, "password_hash": user.password_hash}
    # return None

    # For now, returning a dictionary as placeholder functions did
    print(f"Simulating fetch for user: {username}")
    if username == "testuser": # Maintain previous placeholder behavior
        return {"user_id": 1, "username": "testuser", "password_hash": "hashed_password_example"}
    return None


@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({"error": "Missing data. Username, email, and password are required."}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # Basic validation (can be expanded)
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password cannot be empty."}), 400

    new_user = create_user(username, email, password)

    if new_user:
        # In a real scenario, the 'new_user' object returned by a real create_user function
        # would be an ORM object. We'd then serialize it.
        # For now, it's a dict from the placeholder.
        return jsonify({"message": "User registered successfully", "user": {"user_id": new_user.get("user_id"), "username": new_user.get("username"), "email": new_user.get("email")}}), 201
    else:
        return jsonify({"error": "User already exists or failed to create user."}), 409

@app.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not all(key in data for key in ['username', 'password']):
        return jsonify({"error": "Missing data. Username and password are required."}), 400

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"error": "Username and password cannot be empty."}), 400

    user = get_user_by_username(username)

    if user:
        # Simulate password check (actual hash checking commented out)
        # from werkzeug.security import check_password_hash
        # if check_password_hash(user['password_hash'], password):
        # For now, using placeholder logic
        if user['username'] == "testuser" and password == "password123": # Maintain previous placeholder behavior
            return jsonify({"message": "Login successful", "token": "dummy_jwt_token"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    # Initialize the database
    init_db(app, DATABASE_URI)
    app.run(debug=True, host='0.0.0.0', port=5001) # Changed port for clarity if running multiple apps
