from evidence.evidence_analyzer import (
    analyze_claim_against_evidence
)

tests = [

    (
        "The Earth revolves around the Sun.",
        "Earth revolves around the Sun."
    ),

    (
        "The Earth is the center of the solar system.",
        "The Earth revolves around the Sun."
    ),

    (
        "Water freezes at 0 degrees Celsius at standard atmospheric pressure.",
        "Pure water freezes at 0 degrees Celsius at standard atmospheric pressure."
    ),

    (
        "Mount Everest is the highest mountain above sea level.",
        "Mount Everest is the highest mountain above sea level."
    )

]

print("=" * 70)
print("VERIFI NLI ENGINE TEST")
print("=" * 70)

for claim, evidence in tests:

    result = analyze_claim_against_evidence(
        claim,
        evidence
    )

    print()
    print("CLAIM:", claim)
    print("EVIDENCE:", evidence)

    print(
        "Entailment:",
        result["entailment"]
    )

    print(
        "Contradiction:",
        result["contradiction"]
    )

    print(
        "Neutral:",
        result["neutral"]
    )

    print(
        "Final label:",
        result["label"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )
