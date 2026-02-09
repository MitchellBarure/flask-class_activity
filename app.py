#app.py

from flask import Flask, request, jsonify #Creates app, reads query parameters & returns json responses
import time #How long did the analysis take

from algo import run_analysis
from plotter import make_graph_base64

app = Flask(__name__)

#GET endpoint
@app.route("/analyze", methods=["GET"])
def analyze():
    algo = request.args.get("algo")
    n_raw = request.args.get("n")
    steps_raw = request.args.get("steps",10)

    # Validate algo
    if not algo:
        return jsonify({"error": "Missing required query parameter: algo"}), 400

    # Validate n
    try:
        n = int(n_raw)
        if n < 1:
            return jsonify({"error": "n must be a positive integer"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "n must be an integer"}), 400

    # Validate steps
    try:
        steps = int(steps_raw)
        if steps < 1:
            return jsonify({"error": "steps must be a positive integer"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "steps must be an integer"}), 400

    start_time = time.time()

    try:
        analysis = run_analysis(algo, n, steps)
    except ValueError as e:
        return jsonify({
            "error": str(e),
            "supported_algos": ["bubble", "linear", "binary", "nested", "exponential"]
        }), 400

    #Create and return graph as base64-encoded string via plotting function
    graph_base64 = make_graph_base64(
            analysis["sizes"],
            analysis["times"]
        )

    end_time = time.time()

    return jsonify({
            "algo": algo,
            "items": n,
            "steps": steps,
            "start_time": start_time,
            "end_time": end_time,
            "total_time_ms": (end_time - start_time) * 1000,
            "time_complexity": analysis["time_complexity"],
            "graph_base64": graph_base64
        })

if __name__ == "__main__":
    app.run(port=3000, debug=True)

