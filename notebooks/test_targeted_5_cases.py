import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

tests = [
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
        "Mount Everest is the highest mountain above sea level.",
        "Supported"
    ),
    (
        "FALSE-1",
        "Water freezes at 50 degrees Celsius at standard atmospheric pressure.",
        "Contradicted"
    ),
    (
        "UNVERIFIED-1",
        "A newly discovered cave in India contains a city built entirely from gold.",
        "Unverified"
    )
]

print("=" * 70)
print("VERIFI 5-CASE TARGETED TEST")
print("=" * 70)

passed = 0
failed = 0

for name, claim, expected in tests:

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("CLAIM:")
    print(claim)

    evidence = collect_evidence(
        claim,
        max_results_per_query=5,
        max_evidence=5
    )

    analyzed = analyze_evidence(
        claim,
        evidence
    )

    verdict = calculate_claim_verdict(
        analyzed
    )

    actual = verdict.get(
        "verdict",
        "Unverified"
    )

    print("\nEvidence returned:", len(evidence))
    print("EXPECTED:", expected)
    print("ACTUAL:", actual)

    print(
        "Confidence:",
        verdict.get("confidence", 0.0)
    )

    print(
        "Support:",
        verdict.get("support")
    )

    print(
        "Contradiction:",
        verdict.get("contradiction")
    )

    print(
        "Supporting sources:",
        verdict.get("supporting_sources", 0)
    )

    print(
        "Contradicting sources:",
        verdict.get("contradicting_sources", 0)
    )

    if actual == expected:

        print("STATUS: PASS")
        passed += 1

    else:

        print("STATUS: FAIL")
        failed += 1

print("\n" + "=" * 70)
print("FINAL 5-CASE SUMMARY")
print("=" * 70)

print("Passed:", passed)
print("Failed:", failed)
print("Total:", len(tests))
print(
    "Accuracy:",
    round(
        passed / len(tests) * 100,
        1
    ),
    "%"
)
