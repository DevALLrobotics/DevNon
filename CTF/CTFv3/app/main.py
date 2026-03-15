from __future__ import annotations

import json
from typing import Any, Dict, List
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS

SCORE_PER_TEST = 100
FLAG_VALUE = "flag{flask_ctf_v3}"


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def healthcheck() -> Any:
        return jsonify({"status": "ok"})

    @app.route("/score", methods=["POST"])
    def score_submission() -> Any:
        payload = parse_json_body()
        if payload is None:
            return error_response("Request body must be valid JSON.", 400)

        testcase_results = payload.get("testcase_results")
        if not isinstance(testcase_results, list) or not testcase_results:
            return error_response("Field 'testcase_results' must be a non-empty list.", 400)

        normalized: List[bool] = []
        for idx, value in enumerate(testcase_results, 1):
            if isinstance(value, bool):
                normalized.append(value)
            else:
                return error_response(
                    f"testcase_results[{idx}] must be a boolean value.", 400
                )

        total_tests = len(normalized)
        passed_tests = sum(1 for result in normalized if result)
        score = passed_tests * SCORE_PER_TEST
        flag = FLAG_VALUE if passed_tests == total_tests else None

        return jsonify(
            {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "score": score,
                "flag": flag,
            }
        )

    @app.route("/submit", methods=["POST"])
    def submit_code() -> Any:
        payload = parse_json_body()
        if payload is None:
            return error_response("Request body must be valid JSON.", 400)

        challenge_id = payload.get("challenge_id")
        source_code = payload.get("source_code")

        if not isinstance(challenge_id, str) or not challenge_id.strip():
            return error_response("Field 'challenge_id' must be a non-empty string.", 400)
        if not isinstance(source_code, str) or not source_code.strip():
            return error_response("Field 'source_code' must be a non-empty string.", 400)

        reference_id = f"SUB-{uuid4().hex[:10].upper()}"
        message = (
            "Submission received. Automatic judging is not yet implemented; "
            "please review the queued reference ID for manual verification."
        )

        return jsonify(
            {
                "challenge_id": challenge_id,
                "status": "queued",
                "message": message,
                "reference_id": reference_id,
            }
        )

    return app


def parse_json_body() -> Dict[str, Any] | None:
    if not request.data:
        return {}
    try:
        return json.loads(request.data)
    except json.JSONDecodeError:
        return None


def error_response(message: str, status: int) -> Any:
    response = jsonify({"detail": message})
    response.status_code = status
    return response


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
