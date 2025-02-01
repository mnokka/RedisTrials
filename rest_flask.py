from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Yhdistetään Redis-palvelimeen
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/time', methods=['POST'])
def push_time():
    """
    Ajanottolaite lähettää ajan tietylle kilpailijalle (BIB-numero).
    JSON-muoto: {"bib": "123", "checkpoint": "split_1", "time": 13.50}
    """
    data = request.json
    bib = data.get("bib")
    checkpoint = data.get("checkpoint")
    timestamp = data.get("time")

    if not bib or not checkpoint or not timestamp:
        return jsonify({"error": "Missing data"}), 400

    r.hset(f"race:{bib}", checkpoint, timestamp)
    
    return jsonify({"message": f"Time {timestamp} saved for {bib} at {checkpoint}"}), 201


@app.route('/times/<bib_number>', methods=['GET'])
def get_times(bib_number):
    """
    Hakee tietyn kilpailijan ajanottotiedot.
    """
    times = r.hgetall(f"race:{bib_number}")
    if not times:
        return jsonify({"error": "No data found"}), 404

    return jsonify(times)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
