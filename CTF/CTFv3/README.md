## CTFv3 FastAPI Scoring Service

This API mirrors the scoring logic used by the judge. Each `true` in the `testcase_results` array counts for 100 points and a flag is returned when every test passes.

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the server

```bash
uvicorn app.main:app --reload
```

The API enables permissive CORS for local development, so the static site can call it from another port.

### Frontend

Static site files live in `web/`. You can open `web/index.html` directly in a browser, or serve the directory via any static server (e.g. `python3 -m http.server`).

### Example request

```bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d '{"testcase_results": [true, false, true]}'
```

Response:

```json
{
  "total_tests": 3,
  "passed_tests": 2,
  "score": 200,
  "flag": null
}
```

When all items are `true`, the response includes the flag `"flag": "flag{fastapi_ctf_v3}"`.

### Code submissions

The frontend’s **Submit Code** button calls:

```http
POST /submit
Content-Type: application/json

{
  "challenge_id": "sum-unique",
  "source_code": "...user code...",
  "language": "python"
}
```

Right now the API simply acknowledges the payload and returns a queued reference ID. Hook this endpoint into your judge or storage layer to enable fully automated grading.
