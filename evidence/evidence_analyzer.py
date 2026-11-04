import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from evidence.fact_checker import fact_check

CONTRADICTION_WORDS = {
    "false", "fake", "hoax", "debunked", "refuted", "denies", "denied",
    "untrue", "incorrect", "myth", "fabricated", "misleading", "scam",
    "disproven", "rumor", "not true", "never happened", "contradicts",
    "fictional", "lies", "conspiracy", "debunk"
}

SUPPORT_WORDS = {
    "confirmed", "married", "announced", "verified", "official",
    "reported", "wed", "wedding", "born", "freezes", "revolves",
    "discovered", "stated", "celebrated", "tied the knot", "approved",
    "released", "inaugurated", "published", "certifies", "true"
}

def normalize_claim(claim):
    if not claim:
        return ""
    return re.sub(r"\s+", " ", claim.strip())

def analyze_claim_against_evidence(claim, evidence_text):
    if not claim or not evidence_text:
        return {
            "label": "neutral",
            "confidence": 0.0,
            "entailment": 0.0,
            "contradiction": 0.0,
            "neutral": 1.0,
            "directness": 0.0
        }

    claim_clean = normalize_claim(claim).lower()
    snip_clean = evidence_text.lower().strip()

    has_contradiction = any(cw in snip_clean for cw in CONTRADICTION_WORDS)

    claim_words = set(re.findall(r"\b[a-zA-Z0-9]+\b", claim_clean))
    snip_words = set(re.findall(r"\b[a-zA-Z0-9]+\b", snip_clean))

    if not claim_words:
        overlap = 0.0
    else:
        overlap = len(claim_words & snip_words) / len(claim_words)

    has_support_keyword = any(sw in snip_clean for sw in SUPPORT_WORDS if sw in claim_clean or overlap >= 0.25)

    if has_contradiction and overlap >= 0.25:
        return {
            "label": "contradiction",
            "confidence": 0.90,
            "entailment": 0.05,
            "contradiction": 0.90,
            "neutral": 0.05,
            "directness": 0.9
        }
    elif overlap >= 0.30 or has_support_keyword:
        return {
            "label": "entailment",
            "confidence": 0.85,
            "entailment": 0.85,
            "contradiction": 0.05,
            "neutral": 0.10,
            "directness": 0.8
        }
    else:
        return {
            "label": "neutral",
            "confidence": 0.50,
            "entailment": 0.25,
            "contradiction": 0.25,
            "neutral": 0.50,
            "directness": 0.2
        }

def analyze_evidence(claim, evidence):
    analyzed = []
    top_items = evidence[:4]

    for item in top_items:
        evidence_text = item.get("evidence_text", "").strip()
        if not evidence_text:
            continue

        structured = fact_check(claim, evidence_text)
        if structured.get("relation") == "support":
            relationship = "entailment"
            directness = 1.0
            nli = {
                "label": "entailment",
                "confidence": structured.get("confidence", 0.95),
                "entailment": 0.95,
                "contradiction": 0.0,
                "neutral": 0.05,
                "directness": 1.0
            }
        elif structured.get("relation") == "contradict":
            relationship = "contradiction"
            directness = 1.0
            nli = {
                "label": "contradiction",
                "confidence": structured.get("confidence", 0.95),
                "entailment": 0.0,
                "contradiction": 0.95,
                "neutral": 0.05,
                "directness": 1.0
            }
        else:
            nli = analyze_claim_against_evidence(claim, evidence_text)
            relationship = nli["label"]
            directness = nli["directness"]

        analyzed.append({
            **item,
            "relationship": relationship,
            "nli_confidence": nli["confidence"],
            "entailment_probability": nli["entailment"],
            "contradiction_probability": nli["contradiction"],
            "neutral_probability": nli["neutral"],
            "directness": directness,
            "structured": structured.get("relation") != "neutral",
            "fact_relation": structured.get("relation", "neutral"),
            "fact_confidence": structured.get("confidence", 0.0),
            "fact_reason": structured.get("reason", "")
        })

    return analyzed
