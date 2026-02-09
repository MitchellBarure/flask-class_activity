#app.py

from flask import Flask, request, jsonify #Creates app, reads query parameters & returns json responses
import time #How long did the analysis take

from flask_sqlalchemy import SQLAlchemy

from algo import run_analysis
from plotter import make_graph_base64

app = Flask(__name__)

#Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flask_user:flask_pass123@localhost:3306/algo_analysis_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Analysis results tABLE
class AnalysisResult(db.Model):
    __tablename__ = "analysis_results"

    id = db.Column(db.Integer, primary_key=True)

    algo = db.Column(db.String(50), nullable=False)
    items = db.Column(db.Integer, nullable=False)
    steps = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.Float, nullable=False)
    total_time_ms = db.Column(db.Float, nullable=False)

    time_complexity = db.Column(db.String(20), nullable=False)

    # Store the base64 image string directly
    graph_base64 = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "algo": self.algo,
            "items": self.items,
            "steps": self.steps,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time_ms": self.total_time_ms,
            "time_complexity": self.time_complexity,
            "graph_base64": self.graph_base64,
        }

#GET endpoint
@app.route("/analyze", methods=["GET"])
def analyze():
    algo = request.args.get("algo")
    n_raw = request.args.get("n")
    steps_raw = request.args.get("steps", "10")

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
            "algo": analysis["algo"],
            "items": n,
            "steps": steps,
            "start_time": start_time,
            "end_time": end_time,
            "total_time_ms": (end_time - start_time) * 1000,
            "time_complexity": analysis["time_complexity"],
            "graph_base64": graph_base64
        })

@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    data = request.get_json()

    # Create a new AnalysisResult object
    result = AnalysisResult(
        algo=data["algo"],
        items=data["items"],
        steps=data["steps"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        total_time_ms=data["total_time_ms"],
        time_complexity=data["time_complexity"],
        graph_base64=data["graph_base64"]
    )

    # Save to database
    db.session.add(result)
    db.session.commit()

    # Return success response
    return jsonify({
        "message": "Analysis saved successfully",
        "id": result.id
    }), 201

@app.route("/retrieve_analysis", methods=["GET"])
def retrieve_analysis():
    analysis_id = request.args.get("id")

    # Find the record by ID
    result = AnalysisResult.query.get(analysis_id)

    # If not found
    if result is None:
        return jsonify({"error": "Analysis not found"}), 404

    # Return the saved data
    return jsonify(result.to_dict()), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3000, debug=True)

