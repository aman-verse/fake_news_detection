import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from evidence.verdict_engine import calculate_claim_verdict

def make_evidence(
    relationship,
    entailment,
    contradiction,
    source_score=100,
    relevance=0.9,
    publisher="test_source"
):

    return {
        "relationship": relationship,
        "entailment_probability": entailment,
        "contradiction_probability": contradiction,
        "source_score": source_score,
        "relevance": relevance,
        "publisher_id": publisher
    }

tests = [

    (
        "DIRECT SUPPORT",
        [
            make_evidence(
                "entailment",
                0.99,
                0.005,
                publisher="nasa.gov"
            )
        ]
    ),

    (
        "DIRECT CONTRADICTION",
        [
            make_evidence(
                "contradiction",
                0.005,
                0.99,
                publisher="source1.com"
            )
        ]
    ),

    (
        "WEAK IMPLICATION",
        [
            make_evidence(
                "entailment",
                0.92,
                0.04,
                relevance=0.2,
                publisher="source1.com"
            )
        ]
    ),

    (
        "MIXED",
        [
            make_evidence(
                "entailment",
                0.90,
                0.05,
                publisher="source1.com"
            ),
            make_evidence(
                "contradiction",
                0.05,
                0.90,
                publisher="source2.com"
            )
        ]
    ),

    (
        "NO STRONG EVIDENCE",
        [
            make_evidence(
                "neutral",
                0.20,
                0.20,
                publisher="source1.com"
            )
        ]
    )
]

print("=" * 70)
print("VERIFI LOCAL VERDICT ENGINE TEST")
print("=" * 70)

for name, evidence in tests:

    result = calculate_claim_verdict(
        evidence
    )

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

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
