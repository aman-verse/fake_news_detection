with open("evidence/source_ranker.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add wikipedia and major domains to TRUSTED_NEWS_SCORES
domains_to_add = '''    "wikipedia.org": 94,
    "en.wikipedia.org": 94,
    "indiatimes.com": 90,
    "espn.com": 90,
    "espncricinfo.com": 90,
    "cricbuzz.com": 88,
    "usatoday.com": 90,
    "foxnews.com": 88,
    "time.com": 92,
    "reuters.com": 98,'''

content = content.replace('"reuters.com": 98,', domains_to_add)

# Improve classify_source to recognize news and org domains intelligently
old_classify_end = '''    for trusted_domain in SOCIAL_DOMAINS:

        if matches_domain(
            domain,
            trusted_domain
        ):

            return "Social Media", 45

    return "Other", 30'''

new_classify_end = '''    for trusted_domain in SOCIAL_DOMAINS:

        if matches_domain(
            domain,
            trusted_domain
        ):

            return "Social Media", 45

    if any(k in domain for k in ["news", "times", "post", "tribune", "daily", "herald", "journal", "gazette", "wire", "express", "today"]):
        return "Trusted News", 80

    if domain.endswith(".org") or domain.endswith(".edu"):
        return "Trusted News", 85

    return "Web Source", 60'''

content = content.replace(old_classify_end, new_classify_end)

with open("evidence/source_ranker.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated evidence/source_ranker.py")

