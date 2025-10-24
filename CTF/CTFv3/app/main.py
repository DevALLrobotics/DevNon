from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

SCORE_PER_TEST = 100
FLAG_VALUE = "flag{fastapi_ctf_v3}"


class Submission(BaseModel):
    testcase_results: List[bool]


class ScoreResponse(BaseModel):
    total_tests: int
    passed_tests: int
    score: int
    flag: str | None = None


class CodeSubmission(BaseModel):
    challenge_id: str = Field(..., description="Identifier of the selected challenge.")
    source_code: str = Field(..., min_length=1, description="Contestant source code.")


class CodeSubmissionResponse(BaseModel):
    challenge_id: str
    status: str
    message: str
    reference_id: str


app = FastAPI(title="CTFv3 Scoring API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck() -> dict:
    return {"status": "ok"}


@app.post("/score", response_model=ScoreResponse)
async def score_submission(payload: Submission) -> ScoreResponse:
    if not payload.testcase_results:
        raise HTTPException(status_code=400, detail="No results provided.")

    total_tests = len(payload.testcase_results)
    passed_tests = sum(1 for result in payload.testcase_results if result)
    score = passed_tests * SCORE_PER_TEST

    flag = FLAG_VALUE if passed_tests == total_tests else None

    return ScoreResponse(
        total_tests=total_tests,
        passed_tests=passed_tests,
        score=score,
        flag=flag,
    )


@app.post("/submit", response_model=CodeSubmissionResponse)
async def submit_code(payload: CodeSubmission) -> CodeSubmissionResponse:
    reference_id = f"SUB-{uuid4().hex[:10].upper()}"

    # This is a placeholder implementation. In a real judge we would compile or run the
    # submission here. For now we simply acknowledge receipt and instruct the client to
    # check back later (or poll another endpoint) for results.
    message = (
        "Submission received. Automatic judging is not yet implemented; "
        "please review the queued reference ID for manual verification."
    )

    return CodeSubmissionResponse(
        challenge_id=payload.challenge_id,
        status="queued",
        message=message,
        reference_id=reference_id,
    )
