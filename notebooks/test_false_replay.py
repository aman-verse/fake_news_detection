import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

claim = (
    "China is currently the world's most populous country, "
    "ahead of India."
)

evidence = [

    {
        "title": "India overtakes China as the world's most populous country | Population Division",
        "domain": "un.org",
        "source_type": "Official",
        "source_score": 100,
        "relevance_score": 0.477,
        "evidence_text": (
            "India overtakes China as the world's most populous country. "
            "China is projected to cede its long-held status as the world's "
            "most populous country to India."
        )
    },

    {
        "title": "India overtakes China to become world's most populous country",
        "domain": "theguardian.com",
        "source_type": "Trusted News",
        "source_score": 93,
        "relevance_score": 0.360,
        "evidence_text": (
            "India has overtaken China as the world's most populous country, "
            "according to UN population estimates."
        )
    },

    {
        "title": "UN DESA Policy Brief No. 153",
        "domain": "desapublications.un.org",
        "source_type": "Official",
        "source_score": 100,
        "relevance_score": 0.240,
        "evidence_text": (
            "India overtakes China as the world's most populous country."
        )
    },

    {
        "title": "India overtakes China as the world's most populous country",
        "domain": "digitallibrary.un.org",
        "source_type": "Official",
        "source_score": 100,
        "relevance_score": 0.182,
        "evidence_text": (
            "India's population is projected to continue to grow for several "
            "decades, whereas China's population has recently begun to decline."
        )
    },

    {
        "title": "Population Clock: World",
        "domain": "census.gov",
        "source_type": "Official",
        "source_score": 100,
        "relevance_score": 0.181,
        "evidence_text": (
            "Most Populous Countries: 1. India 1,429,700,205 "
            "2. China 1,405,918,803."
        )
    },

    {
        "title": "China slams the West as India becomes world's most populous country",
        "domain": "nbcnews.com",
        "source_type": "Trusted News",
        "source_score": 90,
        "relevance_score": 0.269,
        "evidence_text": (
            "India will soon overtake China as the world's most populous "
            "country. Both will have almost 1.43 billion people."
        )
    }
]

print("=" * 70)
print("VERIFI FALSE CLAIM FAST REPLAY")
print("=" * 70)

analyzed = analyze_evidence(
    claim,
    evidence
)

print("\nNLI RESULTS")

for item in analyzed:

    print(
        f"\n{item.get('domain')}"
    )

    print(
        "Relationship:",
        item.get("relationship")
    )

    print(
        "NLI confidence:",
        item.get("nli_confidence")
    )

result = calculate_claim_verdict(
    analyzed
)

print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

print(
    "Verdict:",
    result.get("verdict")
)

print(
    "Confidence:",
    result.get("confidence")
)

print(
    "Support:",
    result.get("support_score")
)

print(
    "Contradiction:",
    result.get("contradiction_score")
)

print(
    "Supporting sources:",
    result.get("supporting_sources")
)

print(
    "Contradicting sources:",
    result.get("contradicting_sources")
)

print(
    "Independent sources:",
    result.get("independent_sources")
)
