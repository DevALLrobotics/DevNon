from flask import Flask, render_template, request, jsonify
from problems import PROBLEMS
from grader import grade_one_problem

app = Flask(__name__)

@app.get("/")
def index():
    # default ปัญหาแรก
    first_key = list(PROBLEMS.keys())[0]
    return render_template("index.html", problems=PROBLEMS, default_key=first_key)

@app.post("/api/run")
def api_run():
    data = request.get_json(force=True)
    problem_key = data.get("problem")
    code = data.get("code", "")
    if problem_key not in PROBLEMS:
        return jsonify({"ok": False, "error": "Unknown problem"}), 400

    result = grade_one_problem(problem_key, code)
    return jsonify({"ok": True, "result": result})

if __name__ == "__main__":
    # dev server
    app.run(host="0.0.0.0", port=5000, debug=True)
