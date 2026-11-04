import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.web_search import search_web

query = (
    "India government education policy "
    "latest announcement"
)

results = search_web(
    query,
    max_results=10
)

print("=" * 60)
print("VERIFI WEB SEARCH TEST")
print("=" * 60)

for number, result in enumerate(
    results,
    start=1
):

    print(f"\n{number}. {result['title']}")
    print(result["url"])

print("\nTotal results:", len(results))
