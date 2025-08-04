from pymongo import MongoClient

# Function to connect to MongoDB
def connect_to_mongodb_for_app():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["melospeech"]
        print("✅ Application successfully connected to MongoDB.")
        return db
    except Exception as e:
        print("MongoDB connection failed:", e)
        return None

def load_profile():
    db = connect_to_mongodb_for_app()
    if db is not None:
        user_data = db.users.find_one({"active": True})
        if user_data:
            print("✅ Active user profile loaded:", user_data["username"])
        else:
            print(" No active user found.")
        return user_data
    return None


def load_profile_by_username(username):
    db = connect_to_mongodb_for_app()
    if db is not None:
        user_data = db.users.find_one({"username": username})
        if user_data:
            print(f"✅ User '{username}' found in database.")
        else:
            print(f" User '{username}' not found in database.")
        return user_data
    return None
