import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_analyzer import (
    analyze_claim_against_evidence,
    normalize_claim_for_nli
)

claim = (
    "India overtakes China for the first time "
    "to become world's most populous country."
)

evidence_tests = [

    (
        "The Guardian",
        "India overtakes China to become world's "
        "most populous country."
    ),

    (
        "United Nations",
        "India to overtake China as world's most "
        "populous country in April 2023, United Nations projects."
    ),

    (
        "UN DESA",
        "India overtakes China as the world's "
        "most populous country."
    ),

    (
        "India Today",
        "India overtakes China, becomes most populous "
        "nation with 142.9 crore people."
    )

]

print("=" * 70)
print("VERIFI POPULATION NLI CONTROLLED TEST")
print("=" * 70)

print("\nCLAIM:")
print(claim)
print("\nNORMALIZED CLAIM:")
print(
    normalize_claim_for_nli(
        claim
    )
)

for name, evidence in evidence_tests:

    print("\n" + "-" * 70)

    print(
        "SOURCE:",
        name
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
        "RELATIONSHIP:",
        result["label"]
    )

    print(
        "CONFIDENCE:",
        result["confidence"]
    )
