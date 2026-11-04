import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from evidence.evidence_analyzer import (
    analyze_claim_against_evidence
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
    ),

    (
        "India has overtaken China to become the world's most populous country.",
        "India has overtaken China as the world's most populous country."
    ),

    (
        "The United Nations was founded in 1945.",
        "The United Nations was founded in 1945."
    )
]

print("=" * 70)
print("VERIFI NLI DIRECTNESS TEST")
print("=" * 70)

for i, (claim, evidence) in enumerate(
    tests,
    start=1
):

    result = analyze_claim_against_evidence(
        claim,
        evidence
    )

    print()
    print("=" * 70)
    print("TEST", i)
    print("=" * 70)

    print("CLAIM:", claim)
    print("EVIDENCE:", evidence)

    print(
        "RESULT:",
        result["label"]
    )

    print(
        "NLI CONFIDENCE:",
        result["confidence"]
    )

    print(
        "ENTAILMENT:",
        result["entailment"]
    )

    print(
        "CONTRADICTION:",
        result["contradiction"]
    )

    print(
        "NEUTRAL:",
        result["neutral"]
    )

    print(
        "DIRECTNESS:",
        result["directness"]
    )
