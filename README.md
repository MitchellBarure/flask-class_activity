Flask Algorithm Analyzer API

This project includes 4 files with different roles:
*app.py - Handles flask, JSON requests and responses.
*algo.py - Implements the algorithms
*plotter.py - This handles the graph creation and base64 encoding
*requirements.txt - This includes all dependencies needed to run the project

What this project does:

This Flask API measures how long an algorithm takes to run across increasing input sizes, generates a runtime graph, and returns the results as JSON.

How to Set it up:
(Run locally)
1) Create and activate a virtual environment

On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

On Mac/Linux:
python3 -m venv venv
source venv/bin/activate

2) Install dependencies
   pip install -r requirements.txt

3) Run the server
   python app.py

Server runs at:
http://127.0.0.1:3000

API Endpoint:
GET /analyze

Runs the selected algorithm and returns timing results + a base64-encoded runtime graph.

Example: http://127.0.0.1:3000/analyze?algo=bubble&n=1000&steps=10

Query Parameters:
- algo (string, required)
- Algorithm to analyze. Supported values:
- bubble (Bubble Sort)
- linear (Linear Search)
- n (integer, required)
- Maximum number of elements to test (input size).
- steps (integer, optional, default = 10)
- Number of measurement points from 1 → n.

JSON Response (success)

Returns a JSON object containing:

- algo: algorithm name used

- items: max input size (n)

- steps: number of steps used

- start_time: request start time (seconds since epoch)

- end_time: request end time (seconds since epoch)

- total_time_ms: total request processing time in milliseconds

- time_complexity: Big-O label for the algorithm

- graph_base64: base64-encoded PNG graph (input size vs time)

Example (shortened):

{
"algo": "bubble",
"items": 1000,
"steps": 10,
"start_time": 1769594530.2674,
"end_time": 1769594531.3236,
"total_time_ms": 1056.16,
"time_complexity": "O(n^2)",
"graph_base64": "iVBORw0KGgoAAA..."
}

Errors:
If an unsupported algorithm is requested, the API returns an error.

Example:
/analyze?algo=binary&n=1000&steps=10

Response:
{
"error": "Algorithm is not supported. Use: bubble or linear"
}

Side Notes:
- The graph is returned as a base64 string so it can be sent inside JSON.
