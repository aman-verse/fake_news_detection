import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.query_builder import build_search_queries
from evidence.web_search import search_web

claim = (
    "Water freezes at 0 degrees Celsius "
    "at standard atmospheric pressure."
)

queries = build_search_queries(
    claim,
    deep=False
)

print("=" * 70)
print("WATER SEARCH TEST")
print("=" * 70)

for i, query in enumerate(queries, 1):

    print(f"\nQUERY {i}:")
    print(query)

    try:

        results = search_web(
            query,
            max_results=5
        )

        print(
            "Results:",
            len(results)
        )

        for result in results[:3]:

            print(
                "-",
                result.get("title", "")
            )

            print(
                "  URL:",
                result.get("url", "")
            )

    except Exception as error:

        print(
            "ERROR:",
            error
        )
