from flask import Flask, jsonify
import redis
import logging

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_visit_count():
    return int(redis_client.get('visit_count') or 0)

def increment_visit_count():
    redis_client.incr('visit_count')

def check_redis_health():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError as e:
        logging.error(f"Error connecting to Redis: {e}")
        return False

@app.route('/')
def hello():
    app.logger.info("Received request to /")
    return jsonify({"message": "hello"})

@app.route('/count')
def count():
    try:
        if not check_redis_health():
            return jsonify({"error": "Unable to connect to Redis"}), 500

        increment_visit_count()
        visit_count = get_visit_count()
        app.logger.info(f"Visit count: {visit_count}")
        return jsonify({"visit_count": visit_count})
    except Exception as e:
        app.logger.error(f"Error in /count endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/health')
def health():
    redis_status = check_redis_health()
    app.logger.info(f"Redis health: {redis_status}")
    return jsonify({"health": redis_status})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        logging.error(f"An error occurred during application startup: {e}")
