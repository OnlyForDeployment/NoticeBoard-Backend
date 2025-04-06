from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Initialize PyMongo
try:
    mongo = PyMongo(app)
    print("MongoDB connected successfully")
except Exception as e:
    print("MongoDB connection failed:", str(e))

# Function to initialize DB with a base document
def initialize_db():
    try:
        notices_collection = mongo.db.notices
        if not notices_collection.find_one({"_id": "notices_doc"}):
            notices_collection.insert_one({"_id": "notices_doc", "notices": []})
            print("Initialized notices_doc in DB")
    except Exception as e:
        print("Failed to initialize DB:", str(e))

# PUT request to add a notice
@app.route('/notice', methods=['PUT'])
def add_notice():
    data = request.get_json()
    notice = data.get("notice")

    if not notice:
        return jsonify({"error": "Notice content is required"}), 400

    mongo.db.notices.update_one(
        {"_id": "notices_doc"},
        {"$push": {"notices": notice}}
    )
    return jsonify({"message": "Notice added successfully"}), 200

# GET request to fetch all notices
@app.route('/notices', methods=['GET'])
def get_notices():
    doc = mongo.db.notices.find_one({"_id": "notices_doc"})
    notices = doc.get("notices", []) if doc else []
    return jsonify(notices), 200


if __name__ == '__main__':
    initialize_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)