import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.query_builder import build_search_queries

claim = (
    "The Government of India announced "
    "a new education policy"
)

queries = build_search_queries(
    claim
)

print("=" * 60)
print("VERIFI QUERY BUILDER TEST")
print("=" * 60)

for number, query in enumerate(
    queries,
    start=1
):

    print(
        f"\nQuery {number}:"
    )

    print(query)

print(
    "\nTotal queries:",
    len(queries)
)
