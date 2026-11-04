import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_engine import (
    collect_evidence
)

from evidence.evidence_analyzer import (
    analyze_evidence
)

from evidence.verdict_engine import (
    calculate_claim_verdict
)

TESTS = [

    (
        "REAL-1",
        "The Earth revolves around the Sun.",
        "Supported"
    ),

    (
        "REAL-2",
        "Water freezes at 0 degrees Celsius at standard atmospheric pressure.",
        "Supported"
    ),

    (
        "REAL-3",
        "The Pacific Ocean is the largest ocean on Earth.",
        "Supported"
    ),

    (
        "REAL-4",
        "The United Nations was founded in 1945.",
        "Supported"
    ),

    (
        "REAL-5",
        "Mount Everest is the highest mountain above sea level.",
        "Supported"
    ),

    (
        "FALSE-1",
        "The Earth is the center of the solar system.",
        "Contradicted"
    ),

    (
        "FALSE-2",
        "The Pacific Ocean is the smallest ocean on Earth.",
        "Contradicted"
    ),

    (
        "FALSE-3",
        "The United Nations was founded in 1955.",
        "Contradicted"
    ),

    (
        "FALSE-4",
        "Mount Everest is located in South America.",
        "Contradicted"
    ),

    (
        "FALSE-5",
        "Water freezes at 50 degrees Celsius at standard atmospheric pressure.",
        "Contradicted"
    ),

    (
        "UNVERIFIED-1",
        "A previously unknown island near Antarctica has a permanent population of 50,000 people.",
        "Unverified"
    ),

    (
        "UNVERIFIED-2",
        "A newly discovered cave in India contains a city built entirely from gold.",
        "Unverified"
    ),

    (
        "UNVERIFIED-3",
        "Scientists have discovered a plant that naturally produces diamonds every night.",
        "Unverified"
    ),

    (
        "UNVERIFIED-4",
        "A private company will build a permanent human settlement on Mars before 2030.",
        "Unverified"
    ),

    (
        "UNVERIFIED-5",
        "Researchers have found a lake beneath the Sahara Desert containing a previously unknown civilization.",
        "Unverified"
    ),

]

print("=" * 70)
print("VERIFI FINAL BATCH TEST")
print("=" * 70)

passed = 0

for test_id, claim, expected in TESTS:

    print("\n" + "=" * 70)
    print(test_id)
    print("=" * 70)

    print("CLAIM:")
    print(claim)

    evidence = collect_evidence(
        claim,
        max_results_per_query=5,
        max_evidence=8
    )

    print(
        "\nEvidence returned:",
        len(evidence)
    )

    analyzed = analyze_evidence(
        claim,
        evidence
    )

    result = calculate_claim_verdict(
        analyzed
    )

    actual = result["verdict"]

    print(
        "EXPECTED:",
        expected
    )

    print(
        "ACTUAL:",
        actual
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

    if actual == expected:

        print("STATUS: PASS")
        passed += 1

    else:

        print("STATUS: FAIL")

print("\n")
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(
    "Passed:",
    passed
)

print(
    "Failed:",
    len(TESTS) - passed
)

print(
    "Total:",
    len(TESTS)
)

print(
    "Accuracy:",
    round(
        passed / len(TESTS) * 100,
        2
    ),
    "%"
)
