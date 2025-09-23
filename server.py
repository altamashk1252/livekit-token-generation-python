# server.py
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify
from livekit import api

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/getToken")
def get_token():
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    # Generate a random room name using uuid
    room_name = f"room-{uuid.uuid4().hex[:8]}"  # e.g., room-1a2b3c4d
    identity = f"user-{uuid.uuid4().hex[:6]}"    # e.g., user-a1b2c3
    display_name = "My Name"

    # Check if keys are set
    if not api_key or not api_secret:
        return jsonify({"error": "LIVEKIT_API_KEY or LIVEKIT_API_SECRET not set"}), 500

    # Create the access token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity(identity) \
        .with_name(display_name) \
        .with_grants(api.VideoGrants(room_join=True, room=room_name))

    # Return as JSON
    return jsonify({
        "token": token.to_jwt(),
        "room": room_name,
        "identity": identity,
        "name": display_name
    })

# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
