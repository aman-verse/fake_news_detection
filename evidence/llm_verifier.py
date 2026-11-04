import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get(
    "OPENAI_API_KEY",
    "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"
)

def verify_with_openai(text: str, evidence_snippets=None):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        context = ""
        if evidence_snippets:
            context = "\nWeb evidence:\n" + "\n".join(evidence_snippets[:4])
        prompt = (
            f"Fact-check this news headline or claim. Decide strictly whether it is REAL or FAKE.\n"
            f"Claim: {text}\n{context}\n\n"
            f"Return JSON strictly formatted as:\n"
            f'{{"verdict": "REAL" or "FAKE", "confidence": float between 0.75 and 0.99, "reasoning": "brief explanation"}}'
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional fact-checker. Return only valid JSON with verdict strictly REAL or FAKE."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=150,
            temperature=0.0
        )
        data = json.loads(response.choices[0].message.content)
        verdict = str(data.get("verdict", "REAL")).strip().upper()
        if verdict not in ("REAL", "FAKE"):
            verdict = "REAL"
        confidence = float(data.get("confidence", 0.90))
        return {
            "success": True,
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": data.get("reasoning", "")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

