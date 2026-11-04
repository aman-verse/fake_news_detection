import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.evidence_engine import collect_evidence

claims = [
    "The Earth revolves around the Sun.",
    "Water freezes at 0 degrees Celsius at standard atmospheric pressure.",
    "Mount Everest is the highest mountain above sea level."
]

for claim in claims:

    print("\n" + "=" * 70)
    print("CLAIM:")
    print(claim)

    evidence = collect_evidence(
        claim,
        max_results_per_query=5,
        max_evidence=5,
        deep=False,
        source_scope="Trusted news + official sources"
    )

    print(
        "Evidence returned:",
        len(evidence)
    )

    for item in evidence:

        print(
            "\nTitle:",
            item.get("title", "")
        )

        print(
            "Domain:",
            item.get("domain", "")
        )

        print(
            "Source score:",
            item.get("source_score", 0)
        )

        print(
            "Relevance:",
            item.get("relevance_score", 0)
        )
