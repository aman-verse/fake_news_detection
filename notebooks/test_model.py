import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from models.predictor import predict_news

news = """
The government announced a new education policy
that will provide additional financial support to students.
"""

result = predict_news(news)

print()
print("=" * 50)
print("VERIFI MODEL TEST")
print("=" * 50)

print("\nNews:")
print(news)

print("\nPrediction:", result)

print("=" * 50)
