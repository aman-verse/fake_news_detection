import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

TEST_CASES = [

    {
        "id": "REAL-1",
        "expected": "Supported",
        "claim": (
            "India has overtaken China to become "
            "the world's most populous country."
        )
    },

    {
        "id": "FALSE-1",
        "expected": "Contradicted",
        "claim": (
            "China is currently the world's most "
            "populous country, ahead of India."
        )
    },

    {
        "id": "UNVERIFIED-1",
        "expected": "Unverified",
        "claim": (
            "A newly discovered island near Antarctica "
            "has a permanent population of 50,000 people."
        )
    },

    {
        "id": "MIXED-1",
        "expected": "Contradicted",
        "claim": (
            "India's population is exactly 1.5 billion"
            "within the next few years."
        )
    }
]

print("=" * 70)
print("VERIFI BLIND VERIFICATION TEST")
print("=" * 70)

passed = 0
failed = 0

for test in TEST_CASES:

    print("\n" + "=" * 70)

    print(
        "TEST:",
        test["id"]
    )

    print(
        "CLAIM:",
        test["claim"]
    )

    print(
        "EXPECTED:",
        test["expected"]
    )

    evidence = collect_evidence(
        test["claim"],
        max_results_per_query=5,
        max_evidence=10,
        deep=False,
        source_scope="Trusted news + official sources"
    )

    print(
        "Evidence returned:",
        len(evidence)
    )

    analyzed = analyze_evidence(
        test["claim"],
        evidence
    )

    result = calculate_claim_verdict(
        analyzed
    )

    actual = result.get(
        "verdict",
        "Unverified"
    )

    print(
        "ACTUAL:",
        actual
    )

    print(
        "Confidence:",
        result.get(
            "confidence",
            0
        )
    )

    print(
        "Support:",
        result.get(
            "support_score",
            0
        )
    )

    print(
        "Contradiction:",
        result.get(
            "contradiction_score",
            0
        )
    )

    print(
        "Supporting sources:",
        result.get(
            "supporting_sources",
            0
        )
    )

    print(
        "Contradicting sources:",
        result.get(
            "contradicting_sources",
            0
        )
    )

    if actual == test["expected"]:

        print("STATUS: PASS")

        passed += 1

    else:

        print("STATUS: FAIL")

        failed += 1

print("\n" + "=" * 70)
print("FINAL TEST SUMMARY")
print("=" * 70)

print(
    "Passed:",
    passed
)

print(
    "Failed:",
    failed
)

print(
    "Total:",
    len(TEST_CASES)
)
