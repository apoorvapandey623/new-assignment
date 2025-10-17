from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('flask_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Request latency seconds', ['endpoint'])

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_request(response):
    latency = time.time() - getattr(request, "start_time", time.time())
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
    return response

@app.route('/')
def index():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/about')
def about():
    return jsonify({"about": "This is a Flask app instrumented with Prometheus metrics."})

@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics
    resp = generate_latest()
    return resp, 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
