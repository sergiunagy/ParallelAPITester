from flask import Flask, request, jsonify
# CORS library
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ################# PUBLIC ROUTINES  #########################
@app.route('/test/<ssid>/<data>', methods=["GET"], strict_slashes=False)
def test_api(ssid, data):
    print("Mirroring test")

    return {
        "result": "mirroring-test",
        "message": "Alive",
        "ssid": ssid,
        "data": data,
    }
