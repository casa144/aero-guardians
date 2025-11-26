from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "Server is running"

@app.route("/data")
def get_data():
    dummy_data = {
        "status":"running",
        "message":"successfully ran",
        "users": [
            {"id": 1, "name": "user1"},
            {"id": 2, "name": "user2"}
        ]
    }
    return jsonify



if __name__ in "__main__":
    app.run(debug=True)