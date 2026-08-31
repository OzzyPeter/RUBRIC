import json
import os

from google import genai

_client = None

MODEL_NAME = "gemini-2.5-flash"


def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to your .env file (see .env.example)."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def generate_ai_grade(assignment_title, description, deadline, submission_content):
    """
    Ask Gemini to suggest a grade + feedback for a submission.

    NOTE: this app only stores whatever string the student sent as `file`
    (a filename or, if you have them submit it that way, the actual answer
    text). Gemini can only grade what it's given here — for meaningful
    grading, have students submit real text content, not just a filename.

    Returns (grade: float | None, feedback: str).
    """
    client = get_client()

    prompt = f"""You are grading a student assignment submission for a university course.

Assignment title: {assignment_title}
Assignment description: {description}
Deadline: {deadline}

Student submission:
{submission_content}

Grade the submission on a scale of 0-100 based on how well it satisfies the
assignment description. Respond with ONLY valid JSON, no markdown fences, no
other text, in exactly this shape:
{{"grade": <number 0-100>, "feedback": "<2-3 sentences of constructive feedback>"}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    raw = (response.text or "").strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        data = json.loads(raw)
        grade = float(data["grade"])
        feedback = str(data["feedback"])
        return grade, feedback
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        return None, f"AI grading did not return valid output: {raw[:200]}"