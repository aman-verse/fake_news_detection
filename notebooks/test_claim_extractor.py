import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from nlp.claim_extractor import extract_claims

text = """
World India overtakes China for the first time to become world's
most populous country. India has overtaken China as the world's
most populous country. Population has grown by almost 200 million
since the last census. According to UN estimates, India will
continue to experience population growth over the next decade.
"""

claims = extract_claims(
    text
)

print("=" * 70)
print("VERIFI CLAIM EXTRACTION TEST")
print("=" * 70)

print(
    "\nTotal claims:",
    len(claims)
)

for i, claim in enumerate(
    claims,
    start=1
):

    print(
        f"\nClaim {i}:"
    )

    print(
        claim
    )
