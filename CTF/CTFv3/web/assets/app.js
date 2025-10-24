const form = document.getElementById("score-form");
const challengeListEl = document.getElementById("challenge-items");
const problemTitleEl = document.getElementById("problem-title");
const problemDescriptionEl = document.getElementById("problem-description");
const problemMetaEl = document.getElementById("problem-meta");
const problemDifficultyEl = document.getElementById("problem-difficulty");
const problemCategoryEl = document.getElementById("problem-category");
const sampleInputEl = document.getElementById("problem-sample-input");
const sampleOutputEl = document.getElementById("problem-sample-output");
const codeEditor = document.getElementById("code-editor");
const loadTemplateButton = document.getElementById("load-template");
const clearEditorButton = document.getElementById("clear-editor");
const submitCodeButton = document.getElementById("submit-code");
const submissionStatusEl = document.getElementById("submission-status");
const responseContainer = document.getElementById("response");
const totalTestsEl = document.getElementById("total-tests");
const passedTestsEl = document.getElementById("passed-tests");
const scoreEl = document.getElementById("score");
const flagWrapper = document.querySelector(".flag");
const flagValueEl = document.getElementById("flag-value");
const errorEl = document.getElementById("error-message");

const API_BASE_URL = "http://127.0.0.1:8000";
const STORAGE_PREFIX = "ctfv3-code-";

let activeChallengeId = null;
let challenges = [];

function difficultyClass(difficulty) {
  switch ((difficulty || "").toLowerCase()) {
    case "easy":
      return "difficulty-easy";
    case "medium":
      return "difficulty-medium";
    case "hard":
      return "difficulty-hard";
    default:
      return "";
  }
}

function storageKey(challengeId) {
  return `${STORAGE_PREFIX}${challengeId}`;
}

function getStoredCode(challengeId) {
  try {
    return localStorage.getItem(storageKey(challengeId));
  } catch {
    return null;
  }
}

function saveCode(challengeId, code) {
  try {
    localStorage.setItem(storageKey(challengeId), code);
  } catch {
    // ignore storage errors (e.g., disabled storage)
  }
}

function clearStoredCode(challengeId) {
  try {
    localStorage.removeItem(storageKey(challengeId));
  } catch {
    // ignore storage errors
  }
}

function renderChallengeList(items) {
  challengeListEl.innerHTML = "";
  items.forEach((challenge) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.challengeId = challenge.id;
    button.innerHTML = `
      <span>${challenge.title}</span>
      <span class="difficulty-chip ${difficultyClass(challenge.difficulty)}">${challenge.difficulty}</span>
    `;
    button.addEventListener("click", () => selectChallenge(challenge.id));
    li.appendChild(button);
    challengeListEl.appendChild(li);
  });
}

function highlightActiveChallenge() {
  const buttons = challengeListEl.querySelectorAll("button");
  buttons.forEach((btn) => {
    if (btn.dataset.challengeId === activeChallengeId) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

function selectChallenge(challengeId) {
  const challenge = challenges.find((item) => item.id === challengeId);
  if (!challenge) return;

  activeChallengeId = challengeId;
  highlightActiveChallenge();

  problemTitleEl.textContent = challenge.title;
  problemDescriptionEl.textContent = challenge.description;
  problemDifficultyEl.textContent = challenge.difficulty;
  problemCategoryEl.textContent = challenge.category;
  sampleInputEl.textContent = challenge.sample_input;
  sampleOutputEl.textContent = challenge.sample_output;
  problemMetaEl.classList.remove("hidden");

  const stored = getStoredCode(challengeId);
  if (stored !== null) {
    codeEditor.value = stored;
  } else {
    codeEditor.value = challenge.starter_code;
  }
  codeEditor.dataset.template = challenge.starter_code;
}

async function loadChallenges() {
  try {
    const res = await fetch("assets/challenges.json");
    if (!res.ok) throw new Error("Unable to load challenge data.");
    challenges = await res.json();
    renderChallengeList(challenges);
    if (challenges.length > 0) {
      selectChallenge(challenges[0].id);
    }
  } catch (error) {
    problemTitleEl.textContent = "Unable to load challenges";
    problemDescriptionEl.textContent =
      "Check that assets/challenges.json is available or refresh the page.";
    console.error(error);
  }
}

loadTemplateButton.addEventListener("click", () => {
  if (!activeChallengeId) return;
  const challenge = challenges.find((item) => item.id === activeChallengeId);
  if (!challenge) return;
  codeEditor.value = challenge.starter_code;
  saveCode(activeChallengeId, challenge.starter_code);
});

clearEditorButton.addEventListener("click", () => {
  if (!activeChallengeId) return;
  codeEditor.value = "";
  clearStoredCode(activeChallengeId);
});

submitCodeButton.addEventListener("click", async () => {
  if (!activeChallengeId) {
    submissionStatusEl.textContent = "Please select a challenge first.";
    submissionStatusEl.classList.remove("hidden");
    submissionStatusEl.classList.add("error");
    return;
  }

  const trimmedSource = codeEditor.value.trim();
  if (!trimmedSource) {
    submissionStatusEl.textContent = "Editor is empty. Paste or write your solution before submitting.";
    submissionStatusEl.classList.remove("hidden");
    submissionStatusEl.classList.add("error");
    return;
  }

  submissionStatusEl.textContent = "Submitting...";
  submissionStatusEl.classList.remove("hidden", "error");

  try {
    const res = await fetch(`${API_BASE_URL}/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        challenge_id: activeChallengeId,
        source_code: trimmedSource,
      }),
    });

    const payload = await res.json();

    if (!res.ok) {
      const detail = payload.detail || "Submission failed.";
      throw new Error(detail);
    }

    submissionStatusEl.textContent = `Submission queued (ref: ${payload.reference_id}).`;
  } catch (error) {
    submissionStatusEl.textContent = error.message;
    submissionStatusEl.classList.add("error");
  }
});

codeEditor.addEventListener("input", (event) => {
  if (!activeChallengeId) return;
  saveCode(activeChallengeId, event.target.value);
});

function parseBooleanTokens(raw) {
  return raw
    .split(",")
    .map((token) => token.trim().toLowerCase())
    .filter((token) => token.length)
    .map((token) => {
      if (token === "true") return true;
      if (token === "false") return false;
      throw new Error(`Invalid token: ${token}. Use only true or false.`);
    });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorEl.classList.add("hidden");
  flagWrapper.classList.add("hidden");

  const rawInput = event.target.results.value;
  let testcaseResults;

  try {
    testcaseResults = parseBooleanTokens(rawInput);
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
    responseContainer.classList.remove("hidden");
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/score`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ testcase_results: testcaseResults }),
    });

    const payload = await res.json();

    if (!res.ok) {
      const detail = payload.detail || "Unknown error";
      throw new Error(detail);
    }

    totalTestsEl.textContent = payload.total_tests;
    passedTestsEl.textContent = payload.passed_tests;
    scoreEl.textContent = payload.score;

    if (payload.flag) {
      flagValueEl.textContent = payload.flag;
      flagWrapper.classList.remove("hidden");
    } else {
      flagWrapper.classList.add("hidden");
    }

    responseContainer.classList.remove("hidden");
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("hidden");
    responseContainer.classList.remove("hidden");
  }
});

window.addEventListener("DOMContentLoaded", () => {
  loadChallenges();
});
