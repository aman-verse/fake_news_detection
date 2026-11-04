import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from nlp.claim_extractor import extract_claims

ocr_text = """
World India overtakes China for ala first time to become world's most populous country population has grown by almost India has overtaken China as the 200 million - greater than the popu- lation of Brazil - since the last census Hannah Ellis-Petersen world's most populous country in 2o11, and experts say the lack of South Asia correspondent Population estimates for 1 July each year to vital data is hindering policymaking 2021 and medium variant projections thereafter and welfare programmes. India has overtaken China as the 2 billion India's demographyisfarfromuni- 2064 peak 1.7 billion form across the country. One third of world's most populous coun- predictedpopulation growth over the according to UN estimates, India 1.5 next decade will come from just two
"""

claims = extract_claims(ocr_text)

print("=" * 70)
print("CURRENT OCR CLAIM EXTRACTION")
print("=" * 70)

for i, claim in enumerate(claims, 1):
    print(f"\nCLAIM {i}:")
    print(claim)
