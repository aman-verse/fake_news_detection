import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.web_search import search_web
from evidence.source_ranker import rank_sources

query = (
    "India government education policy "
    "latest announcement"
)

results = search_web(
    query,
    max_results=10
)

ranked_results = rank_sources(
    results
)

print("=" * 70)
print("VERIFI SOURCE RANKING TEST")
print("=" * 70)

for number, result in enumerate(
    ranked_results,
    start=1
):

    print(
        f"\n{number}. "
        f"{result['title']}"
    )

    print(
        "Domain:",
        result["domain"]
    )

    print(
        "Type:",
        result["source_type"]
    )

    print(
        "Score:",
        result["source_score"]
    )

    print(
        "URL:",
        result["url"]
    )

print(
    "\nTotal sources:",
    len(ranked_results)
)
