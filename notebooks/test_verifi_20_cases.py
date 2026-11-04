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
        "claim": "The Earth revolves around the Sun."
    },

    {
        "id": "REAL-2",
        "expected": "Supported",
        "claim": "Water freezes at 0 degrees Celsius at standard atmospheric pressure."
    },

    {
        "id": "REAL-3",
        "expected": "Supported",
        "claim": "The Pacific Ocean is the largest ocean on Earth."
    },

    {
        "id": "REAL-4",
        "expected": "Supported",
        "claim": "The United Nations was founded in 1945."
    },

    {
        "id": "REAL-5",
        "expected": "Supported",
        "claim": "Mount Everest is the highest mountain above sea level."
    },

    {
        "id": "FALSE-1",
        "expected": "Contradicted",
        "claim": "The Earth is the center of the solar system."
    },

    {
        "id": "FALSE-2",
        "expected": "Contradicted",
        "claim": "The Pacific Ocean is the smallest ocean on Earth."
    },

    {
        "id": "FALSE-3",
        "expected": "Contradicted",
        "claim": "The United Nations was founded in 1955."
    },

    {
        "id": "FALSE-4",
        "expected": "Contradicted",
        "claim": "Mount Everest is located in South America."
    },

    {
        "id": "FALSE-5",
        "expected": "Contradicted",
        "claim": "Water freezes at 50 degrees Celsius at standard atmospheric pressure."
    },

    {
        "id": "UNVERIFIED-1",
        "expected": "Unverified",
        "claim": "A previously unknown island near Antarctica has a permanent population of 50,000 people."
    },

    {
        "id": "UNVERIFIED-2",
        "expected": "Unverified",
        "claim": "A newly discovered cave in India contains a city built entirely from gold."
    },

    {
        "id": "UNVERIFIED-3",
        "expected": "Unverified",
        "claim": "Scientists have discovered a plant that naturally produces diamonds every night."
    },

    {
        "id": "UNVERIFIED-4",
        "expected": "Unverified",
        "claim": "A private company will build a permanent human settlement on Mars before 2030."
    },

    {
        "id": "UNVERIFIED-5",
        "expected": "Unverified",
        "claim": "Researchers have found a lake beneath the Sahara Desert containing a previously unknown civilization."
    },

    {
        "id": "MIXED-1",
        "expected": "Unverified",
        "claim": "The global population will reach exactly 9 billion on January 1, 2032."
    },

    {
        "id": "MIXED-2",
        "expected": "Unverified",
        "claim": "India will have exactly 1.6 billion people in the year 2050."
    },

    {
        "id": "MIXED-3",
        "expected": "Unverified",
        "claim": "Artificial intelligence will replace exactly 50 percent of all jobs worldwide by 2035."
    },

    {
        "id": "MIXED-4",
        "expected": "Unverified",
        "claim": "The average global temperature will increase by exactly 2.37 degrees Celsius by 2040."
    },

    {
        "id": "MIXED-5",
        "expected": "Unverified",
        "claim": "Humans will establish a permanent settlement on Mars with more than 1,000 residents by 2040."
    }
]

print("=" * 70)
print("VERIFI 20-CASE BLIND VERIFICATION TEST")
print("=" * 70)

results = []

for test in TEST_CASES:

    print("\n" + "=" * 70)

    print(
        f"TEST: {test['id']}"
    )

    print(
        f"CLAIM: {test['claim']}"
    )

    print(
        f"EXPECTED: {test['expected']}"
    )

    try:

        evidence = collect_evidence(
            test["claim"],
            max_results_per_query=5,
            max_evidence=5,
            deep=False,
            source_scope="Trusted news + official sources"
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

        passed = (
            actual == test["expected"]
        )

        results.append(
            passed
        )

        print(
            "Evidence returned:",
            len(evidence)
        )

        print(
            "ACTUAL:",
            actual
        )

        print(
            "Confidence:",
            result.get(
                "confidence",
                0.0
            )
        )

        print(
            "Support:",
            result.get(
                "support_score",
                0.0
            )
        )

        print(
            "Contradiction:",
            result.get(
                "contradiction_score",
                0.0
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

        print(
            "STATUS:",
            "PASS" if passed else "FAIL"
        )

    except Exception as error:

        results.append(False)

        print(
            "ERROR:",
            error
        )

        print(
            "STATUS: FAIL"
        )

passed_count = sum(
    results
)

failed_count = (
    len(results)
    - passed_count
)

print("\n" + "=" * 70)
print("FINAL 20-CASE SUMMARY")
print("=" * 70)

print(
    "Passed:",
    passed_count
)

print(
    "Failed:",
    failed_count
)

print(
    "Total:",
    len(results)
)

print(
    "Accuracy:",
    round(
        passed_count / len(results) * 100,
        1
    ),
    "%"
)
