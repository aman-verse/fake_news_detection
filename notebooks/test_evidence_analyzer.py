import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_analyzer import (
    analyze_claim_against_evidence
)

claim = (
    "Virat Kohli is alive and continues "
    "to play cricket."
)

tests = [

    (
        "Virat Kohli is alive.",
        "Virat Kohli is alive."
    ),

    (
        "Virat Kohli is alive.",
        "Virat Kohli died."
    ),

    (
        "Virat Kohli is alive.",
        "Virat Kohli is a famous Indian cricketer."
    )

]

for number, (claim, evidence) in enumerate(
    tests,
    start=1
):

    print("\n" + "=" * 70)

    print(
        f"TEST {number}"
    )

    print(
        "CLAIM:",
        claim
    )

    print(
        "EVIDENCE:",
        evidence
    )

    result = analyze_claim_against_evidence(
        claim,
        evidence
    )

    print(
        "RESULT:",
        result["label"]
    )

    print(
        "CONFIDENCE:",
        result["confidence"]
    )

print("=" * 70)
print("VERIFI NLI TEST")
print("=" * 70)

print("\nCLAIM:")
print(claim)

print("\nEVIDENCE:")
print(evidence)

result = analyze_claim_against_evidence(
    claim,
    evidence
)

print("\nRESULT:")
print(
    "Relationship:",
    result["label"]
)

print(
    "Confidence:",
    result["confidence"]
)
