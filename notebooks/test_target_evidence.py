import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.evidence_engine import collect_evidence

CLAIMS = [
    "Water freezes at 0 degrees Celsius at standard atmospheric pressure.",
    "Mount Everest is the highest mountain above sea level.",
    "Water freezes at 50 degrees Celsius at standard atmospheric pressure."
]

for claim in CLAIMS:

    print("\n" + "=" * 70)
    print("CLAIM:")
    print(claim)
    print("=" * 70)

    evidence = collect_evidence(
        claim,
        max_results_per_query=5,
        max_evidence=5
    )

    print(
        "\nEvidence returned:",
        len(evidence)
    )

    for i, item in enumerate(
        evidence,
        start=1
    ):

        print("\n" + "-" * 70)

        print("Evidence:", i)
        print("Title:", item.get("title"))
        print("Domain:", item.get("domain"))
        print("Relevance:", item.get("relevance_score"))
        print("Final score:", item.get("final_score"))

        print("\nEVIDENCE TEXT:")
        print(
            item.get(
                "evidence_text",
                ""
            )
        )
