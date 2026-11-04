import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.query_builder import (
    build_search_queries
)

claim = (
    "Virat Kohli was found dead in a river"
)

print("=" * 70)
print("VERIFI DEEP INVESTIGATION QUERY TEST")
print("=" * 70)

queries = build_search_queries(
    claim,
    deep=True
)

for number, query in enumerate(
    queries,
    start=1
):

    print(
        f"\n{number}. {query}"
    )

print(
    "\nTotal deep queries:",
    len(queries)
)
