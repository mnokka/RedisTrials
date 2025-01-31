from flask import Flask, request, jsonify
import redis
import json
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

#load race timings definition
def load_config():
    try:
        with open("db.config", "r") as f:
            config = json.load(f)
            if 'allowed_checkpoints' in config:
                logging.info("Loaded race time checkpoints: %s", config['allowed_checkpoints'])
                return set(config.get("allowed_checkpoints", []))
            else:
                logging.error("No 'allowed_checkpoints' found in config.")
                return set()
    except Exception as e:
                logging.error("Error loading config: %s", str(e))
                return set()


ALLOWED_CHECKPOINTS = load_config()

@app.route('/time', methods=['POST'])
def push_time():
    """
    Send defined time for Bib number (competitor). Format:
    {
    "bib": "123",
    "times": {
        "start": 10.0,  -->time values configured in db.config
        "split1": 13.50,
        "finish": 15.40
     }  
    }

    curl -X POST http://localhost:5000/time \
     -H "Content-Type: application/json" \
     -d '{"bib": "123", "times": {"start": 10.0, "split1": 13.50, "finish": 15.40}}'

    """
    data = request.json
    bib = data.get("bib")
    times = data.get("times") 

    if not bib or not times:
        logging.error("Error in sent config data format; missing data")
        return jsonify({"error": "Missing data"}), 400

    logging.info(f"Time updates for Bib:{bib}")
    
    # check any missing time checkpoint
    missing_checkpoints = ALLOWED_CHECKPOINTS - set(times.keys())
    if missing_checkpoints:
        logging.error("Missing checkpoints in data: %s", missing_checkpoints)
        return jsonify({"error": f"Missing checkpoints: {', '.join(missing_checkpoints)}"}), 400

    
    #check validity of time checkpoints
    if not set(times.keys()).issubset(ALLOWED_CHECKPOINTS):
        logging.error("Illegal checkpoint(s) in sent times configuration")
        return jsonify({"error": "Invalid checkpoint(s) in request"}), 400

    # -1 skip timing value update
    for checkpoint, timestamp in times.items():
        if timestamp != -1:
            r.hset(f"race:{bib}", checkpoint, timestamp)
            logging.info(f"Updated Bib: {bib} checkpoint: {checkpoint} timestamp: {timestamp}")
    return jsonify({"message": f"Times updated for {bib}"}), 201

@app.route('/times/<bib_number>', methods=['GET'])
def get_times(bib_number):
    """
    Get Bib number timing info
    curl -X GET http://localhost:5000/times/123

    """
    times = r.hgetall(f"race:{bib_number}")
    if not times:
        logging.error(f"Bib: {bib_number} data not found")
        return jsonify({"error": "No data found"}), 404
    logging.info(f"Bib: {bib_number} timing info returned: {times}") 
    return jsonify(times)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
