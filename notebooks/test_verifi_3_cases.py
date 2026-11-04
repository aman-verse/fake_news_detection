import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

TESTS = [

    (
        "REAL",
        "The United Nations was founded in 1945."
    ),

    (
        "FALSE",
        "The United Nations was founded in 1955."
    ),

    (
        "UNVERIFIED",
        "A newly discovered island near Antarctica has "
        "a permanent population of 50,000 people."
    )
]

print("=" * 70)
print("VERIFI 3-CASE INTEGRATION TEST")
print("=" * 70)

for name, claim in TESTS:

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

    print(
        "\nEvidence returned:",
        len(evidence)
    )

    analyzed = analyze_evidence(
        claim,
        evidence
    )

    verdict = calculate_claim_verdict(
        analyzed
    )

    print("\nVERDICT:")
    print(
        verdict.get(
            "verdict"
        )
    )

    print(
        "Confidence:",
        verdict.get(
            "confidence"
        )
    )

    print(
        "Support:",
        verdict.get(
            "support"
        )
    )

    print(
        "Contradiction:",
        verdict.get(
            "contradiction"
        )
    )

    print(
        "Supporting sources:",
        verdict.get(
            "supporting_sources"
        )
    )

    print(
        "Contradicting sources:",
        verdict.get(
            "contradicting_sources"
        )
    )

    print("\nNLI RESULTS:")

    for item in analyzed:

        print(
            item.get(
                "domain",
                ""
            ),
            "->",
            item.get(
                "relationship",
                ""
            ),
            item.get(
                "nli_confidence",
                0
            )
        )
