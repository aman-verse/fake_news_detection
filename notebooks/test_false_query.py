import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.query_builder import build_search_queries

claim = (
    "China is currently the world's most populous country, "
    "ahead of India."
)

print("=" * 70)
print("VERIFI FALSE CLAIM QUERY TEST")
print("=" * 70)

print("\nCLAIM:")
print(claim)

queries = build_search_queries(
    claim,
    deep=False
)

print("\nGENERATED QUERIES:")

for i, query in enumerate(
    queries,
    1
):

    print(
        f"{i}. {query}"
    )
