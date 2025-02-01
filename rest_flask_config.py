# Author: Mika Nokka,  mika.nokka1@gmail.com
# License: MIT
# Date: January 2025

from flask import Flask, request, jsonify
import redis
import json
import logging
import sys

CHECKPOINTS_PATH="db.json"
COMPETITOR_PATH="competitor.json"
REDIS_HOST="localhost"
REDIS_PORT="6379"

# Globals, totally intentionally
ALLOWED_GENDERS=None
ALLOWED_CATEGORIES=None
ALLOWED_COMPETITOR_INFO=None
r = None

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

###################################################################################
# Check Redis server existence
def check_redis_connection():
    global r
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping() 
        logging.info(f"Connected to Redis({REDIS_HOST}:{REDIS_PORT}) successfully.")
    except redis.ConnectionError as e:
        logging.error(f"**** Connection to Redis ({REDIS_HOST}:{REDIS_PORT}) failed: {e} ****")
        logging.error(f"*** Exiting the application ***")
        sys.exit(1)  

####################################################################################
# Load race timings definition
def load_config():
    try:
        with open(CHECKPOINTS_PATH, "r") as f:
            config = json.load(f)
            if 'allowed_checkpoints' in config:
                logging.info("Loaded OK race time checkpoints: %s", config['allowed_checkpoints'])
                return set(config.get("allowed_checkpoints", []))
            else:
                logging.error("No 'allowed_checkpoints' found in config.")
                return set()
    except Exception as e:
                logging.error("Error loading timings config: %s", str(e))
                return set()

#####################################################################################
# Load competitor definitions
def load_competitor():
    try:
        with open(COMPETITOR_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

            if 'competitor_info' in data:
                logging.info("Loaded competitor definitions: %s", data['competitor_info'])
            else:
                logging.error("No 'competitor_info' found in data")
                return None

            allowed_genders = data['competitor_info'].get('allowed_genders', [])  # empty list if not found
            allowed_categories = data['competitor_info'].get('allowed_categories', [])
            allowed_keys = data['competitor_info'].get('allowed_keys', [])

            #either empty or not at all
            if not allowed_genders:
                logging.error("No values found for 'allowed_genders'")
            if not allowed_categories:
                logging.error("No values found for 'allowed_categories'")
            if not allowed_keys:
                logging.error("No values found for 'allowed_keys'")

            if allowed_genders and allowed_categories and allowed_keys:
                logging.info(f"Competitor settings OK.\n allowed_genders:{allowed_genders}\n allowed_categories:{allowed_categories}\n allowed_keys:{allowed_keys}")
                return allowed_genders, allowed_categories, allowed_keys
            else:
                logging.error("One or more required fields are missing values")
                return None, None, None

    except Exception as e:
        logging.error("General data loading error.")
        return None, None, None

# redis is-it-alive check
check_redis_connection()

# flask server startup go/nogo loadings and checking
ALLOWED_CHECKPOINTS = load_config()
if not ALLOWED_CHECKPOINTS:
    logging.error("*** Race checkpoints are invalid. Exiting the application ***")
    sys.exit(1)

ALLOWED_GENDERS,ALLOWED_CATEGORIES,ALLOWED_COMPETITOR_INFO=load_competitor()
if ALLOWED_GENDERS is None or ALLOWED_CATEGORIES is None or ALLOWED_COMPETITOR_INFO is None:
    logging.error("*** Competitor data is invalid. Exiting the application ***")
    sys.exit(1)





#######################################################################################
# REST API SECTION
#######################################################################################

#######################################################################################
# Create competitor
#
@app.route('/competitor', methods=['POST'])
def create_competitor():
    """"
    curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
    "bib": "123",
    "first_name": "Ellen",
    "last_name": "Ripley",
    "gender": "female",
    "country": "USA",
    "category": "women40"
    }' \
    http://localhost:5000/competitor
    """

    data = request.json
  
    missing_keys = [key for key in ALLOWED_COMPETITOR_INFO if key not in data]
    if missing_keys:
        logging.error(f"Competitor creation error. Missing field {', '.join(missing_keys)}")
        return jsonify({"error": f"Missing fields: {', '.join(missing_keys)}"}), 400

    extra_keys = [key for key in data if key not in ALLOWED_COMPETITOR_INFO]
    if extra_keys:
        logging.error(f"Competitor creation error. Extra fields {', '.join(extra_keys)}")
        return jsonify({"error": f"Extra fields: {', '.join(extra_keys)}"}), 400

    if data['gender'] not in ALLOWED_GENDERS:
        logging.error(f"Competitor Gender error: {data['gender']}")
        return jsonify({"error": f"Gender error: {data['gender']}"}), 400

    if data['category'] not in ALLOWED_CATEGORIES:
        logging.error(f"Competitor Category error: {data['category']}")
        return jsonify({"error": f"Category error: {data['category']}"}), 400

    
    try:
        bib_number = data['bib']
        data = {k: str(v) for k, v in data.items()} # change data to strings
        r.hset(f"competitor:{bib_number}", mapping=data)
        logging.info(f"Competitor created ok: {data}")
        return jsonify({"message": "OK. Competitor created ok"}), 201
    
    except KeyError:
        logging.error(f"Competitor creation 'bib' key error {bib_number}")
        return jsonify({"error": "Missing 'bib' key in data"}), 400
    except redis.RedisError as e:
        logging.error(f"Competitor creation Redis error: {e}")
        return jsonify({"error": f"Redis error: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"Unknow Redis error:{e}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

#####################################################################################################
# Update Bib number timing info
#
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
        logging.error(f"Bib:{bib}  Missing checkpoints in data:{missing_checkpoint}")
        return jsonify({"error": f"Missing checkpoints: {', '.join(missing_checkpoints)}"}), 400

    
    #check validity of time checkpoints
    #if not set(times.keys()).issubset(ALLOWED_CHECKPOINTS):
    invalid_checkpoints = [checkpoint for checkpoint in times.keys() if checkpoint not in ALLOWED_CHECKPOINTS]
    if invalid_checkpoints:
        logging.error(f"Bib:{bib}  Invalid checkpoint(s): {', '.join(invalid_checkpoints)} in sent times configuration")
        return jsonify({"error": "Invalid checkpoint(s) in request"}), 400

    # -1 skip timing value update
    for checkpoint, timestamp in times.items():
        if timestamp != -1:
            r.hset(f"race:{bib}", checkpoint, timestamp)
            logging.info(f"Updated Bib: {bib} checkpoint: {checkpoint} timestamp: {timestamp}")
    return jsonify({"message": f"Times updated for {bib}"}), 201

#####################################################################################
# Get Bib number timing info
#
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
