import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.verdict_engine import (
    calculate_claim_verdict,
    calculate_overall_verdict
)

supporting_evidence = [

    {
        "domain": "reuters.com",
        "publisher_id": "reuters",
        "source_score": 98,
        "relevance_score": 0.90,
        "relationship": "entailment",
        "entailment_probability": 0.95,
        "contradiction_probability": 0.01,
        "directness": 1.0
    },

    {
        "domain": "bbc.com",
        "publisher_id": "bbc",
        "source_score": 96,
        "relevance_score": 0.85,
        "relationship": "entailment",
        "entailment_probability": 0.93,
        "contradiction_probability": 0.02,
        "directness": 1.0
    },

    {
        "domain": "apnews.com",
        "publisher_id": "associated_press",
        "source_score": 98,
        "relevance_score": 0.80,
        "relationship": "entailment",
        "entailment_probability": 0.91,
        "contradiction_probability": 0.03,
        "directness": 1.0
    }
]

contradicting_evidence = [

    {
        "domain": "reuters.com",
        "publisher_id": "reuters",
        "source_score": 98,
        "relevance_score": 0.90,
        "relationship": "contradiction",
        "entailment_probability": 0.01,
        "contradiction_probability": 0.96,
        "directness": 1.0
    },

    {
        "domain": "bbc.com",
        "publisher_id": "bbc",
        "source_score": 96,
        "relevance_score": 0.85,
        "relationship": "contradiction",
        "entailment_probability": 0.02,
        "contradiction_probability": 0.94,
        "directness": 1.0
    },

    {
        "domain": "apnews.com",
        "publisher_id": "associated_press",
        "source_score": 98,
        "relevance_score": 0.80,
        "relationship": "contradiction",
        "entailment_probability": 0.03,
        "contradiction_probability": 0.92,
        "directness": 1.0
    }
]

mixed_evidence = [

    {
        "domain": "reuters.com",
        "publisher_id": "reuters",
        "source_score": 98,
        "relevance_score": 0.90,
        "relationship": "entailment",
        "entailment_probability": 0.90,
        "contradiction_probability": 0.05,
        "directness": 1.0
    },

    {
        "domain": "bbc.com",
        "publisher_id": "bbc",
        "source_score": 96,
        "relevance_score": 0.90,
        "relationship": "contradiction",
        "entailment_probability": 0.05,
        "contradiction_probability": 0.90,
        "directness": 1.0
    }
]

print("=" * 70)
print("VERIFI VERDICT ENGINE TEST")
print("=" * 70)

for name, evidence in [
    ("STRONG SUPPORT", supporting_evidence),
    ("STRONG CONTRADICTION", contradicting_evidence),
    ("MIXED EVIDENCE", mixed_evidence)
]:

    print(
        "\n" + "=" * 70
    )

    print(
        name
    )

    result = calculate_claim_verdict(
        evidence
    )

    print(
        "Verdict:",
        result["verdict"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Support:",
        result["support_score"]
    )

    print(
        "Contradiction:",
        result["contradiction_score"]
    )

    print(
        "Supporting sources:",
        result["supporting_sources"]
    )

    print(
        "Contradicting sources:",
        result["contradicting_sources"]
    )

assert calculate_claim_verdict(
    supporting_evidence
)["verdict"] == "Supported"

assert calculate_claim_verdict(
    contradicting_evidence
)["verdict"] == "Contradicted"

assert calculate_claim_verdict(
    mixed_evidence
)["verdict"] == "Unverified"

print(
    "\n" + "=" * 70
)

print(
    "OVERALL VERDICT TEST"
)

claim_results = [

    {
        "verdict": "Supported",
        "confidence": 0.91,
        "support_score": 2.5,
        "contradiction_score": 0.0
    },

    {
        "verdict": "Supported",
        "confidence": 0.88,
        "support_score": 2.1,
        "contradiction_score": 0.0
    }

]

overall = calculate_overall_verdict(
    claim_results,
    "Fake"
)

print(
    "Final verdict:",
    overall["verdict"]
)

print(
    "Confidence:",
    overall["confidence"]
)

assert overall["verdict"] == "REAL"

assert calculate_overall_verdict(
    [],
    "Real"
)["verdict"] == "REAL"

assert calculate_overall_verdict(
    [
        {
            "verdict": "Unverified",
            "confidence": 0.0,
            "support_score": 0.0,
            "contradiction_score": 0.0
        }
    ],
    "Fake"
)["verdict"] == "FAKE"

assert calculate_overall_verdict(
    [
        {
            "verdict": "Supported",
            "confidence": 0.7,
            "support_score": 0.7,
            "contradiction_score": 0.0
        },
        {
            "verdict": "Contradicted",
            "confidence": 0.9,
            "support_score": 0.0,
            "contradiction_score": 0.2
        }
    ],
    "Fake"
)["verdict"] == "REAL"

print("Binary verdict fallback tests passed.")
