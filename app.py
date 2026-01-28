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
    n = int(request.args.get("n"))
    steps = int(request.args.get("steps",10))

    start_time = time.time()

    analysis = run_analysis(algo, n, steps)

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

