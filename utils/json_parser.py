import json

REQUIRED_KEYS = [
    "ats_score",
    "strengths",
    "weaknesses",
    "missing_sections",
    "keyword_suggestions",
    "formatting_suggestions",
    "overall_verdict",
]


def parse_json(response: str) -> dict:

    try:

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "")

        response = response.replace("```", "")

        data = json.loads(response)

        return data

    except Exception as error:

        raise ValueError(
            f"Invalid JSON returned by Gemini.\n{error}"
        )