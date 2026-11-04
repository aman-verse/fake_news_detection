from urllib.parse import urlparse

OFFICIAL_DOMAINS = {
    "gov.in",
    "nic.in",
    "gov",
    "mil",
    "edu",
    "edu.in",
    "nasa.gov",
    "noaa.gov",
    "usgs.gov",
    "nist.gov",
    "cdc.gov",
    "nih.gov",
    "who.int",
    "un.org"
}

TRUSTED_NEWS_SCORES = {

        "wikipedia.org": 94,
    "en.wikipedia.org": 94,
    "indiatimes.com": 90,
    "espn.com": 90,
    "espncricinfo.com": 90,
    "cricbuzz.com": 88,
    "usatoday.com": 90,
    "foxnews.com": 88,
    "time.com": 92,
    "reuters.com": 98,
    "apnews.com": 98,
    "bbc.com": 96,
    "bbc.co.uk": 96,
    "npr.org": 95,
    "pbs.org": 95,
    "theguardian.com": 93,
    "nytimes.com": 93,
    "washingtonpost.com": 93,
    "wsj.com": 93,
    "ft.com": 94,
    "economist.com": 92,
    "aljazeera.com": 91,
    "dw.com": 91,
    "france24.com": 90,
    "abcnews.go.com": 90,
    "cbsnews.com": 90,
    "nbcnews.com": 90,
    "cnbc.com": 90,

    "thehindu.com": 94,
    "sportstar.thehindu.com": 94,
    "indianexpress.com": 92,
    "hindustantimes.com": 91,
    "ndtv.com": 91,
    "timesofindia.indiatimes.com": 90,
    "economictimes.indiatimes.com": 90,
    "indiatoday.in": 90,
    "news18.com": 88,
    "moneycontrol.com": 88,
    "business-standard.com": 88,
    "deccanherald.com": 87,
    "telegraphindia.com": 87,
    "theprint.in": 86,
    "firstpost.com": 85,
    "outlookindia.com": 84,

    "snopes.com": 95,
    "politifact.com": 95,
    "factcheck.org": 95,
    "boomlive.in": 94,
    "altnews.in": 94,
    "afp.com": 93,
    "thequint.com": 84,

    "britannica.com": 94,
    "nationalgeographic.com": 93,
    "scientificamerican.com": 92,
    "nature.com": 96,
    "science.org": 96

}

FACT_CHECK_DOMAINS = {
    "snopes.com",
    "politifact.com",
    "factcheck.org",
    "boomlive.in",
    "altnews.in"
}

SOCIAL_DOMAINS = {
    "x.com",
    "twitter.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
    "linkedin.com"
}

def get_domain(url):

    try:

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:

        return ""

def get_publisher_id(domain):

    domain = domain.lower().strip()

    publisher_groups = {
        "bbc": {
            "bbc.com",
            "bbc.co.uk"
        },

        "the_hindu": {
            "thehindu.com",
            "sportstar.thehindu.com"
        },

        "indian_express": {
            "indianexpress.com"
        },

        "economic_times": {
            "economictimes.indiatimes.com"
        },

        "hindustan_times": {
            "hindustantimes.com"
        },

        "reuters": {
            "reuters.com"
        },

        "associated_press": {
            "apnews.com"
        },

        "new_york_times": {
            "nytimes.com"
        },

        "washington_post": {
            "washingtonpost.com"
        },

        "guardian": {
            "theguardian.com"
        },

        "al_jazeera": {
            "aljazeera.com"
        },

        "ndtv": {
            "ndtv.com"
        }
    }

    for publisher, domains in publisher_groups.items():

        if domain in domains:
            return publisher

    return domain

def matches_domain(
    domain,
    trusted_domain
):

    return (
        domain == trusted_domain
        or domain.endswith(
            "." + trusted_domain
        )
    )

def classify_source(url):

    domain = get_domain(url)

    if not domain:

        return "Unknown", 0

    for trusted_domain in OFFICIAL_DOMAINS:

        if matches_domain(
            domain,
            trusted_domain
        ):

            return "Official", 100

    for trusted_domain in FACT_CHECK_DOMAINS:

        if matches_domain(
            domain,
            trusted_domain
        ):

            return "Fact Check", 95

    for trusted_domain, score in TRUSTED_NEWS_SCORES.items():

        if matches_domain(
            domain,
            trusted_domain
        ):

           return "Trusted News", score

    for trusted_domain in SOCIAL_DOMAINS:

        if matches_domain(
            domain,
            trusted_domain
        ):

            return "Social Media", 45

    if any(k in domain for k in ["news", "times", "post", "tribune", "daily", "herald", "journal", "gazette", "wire", "express", "today"]):
        return "Trusted News", 80

    if domain.endswith(".org") or domain.endswith(".edu"):
        return "Trusted News", 85

    return "Web Source", 60

def apply_domain_diversity(
    results,
    max_per_publisher=1
):

    diversified = []

    publisher_counts = {}

    for result in results:

        publisher = result.get(
            "publisher_id",
            result.get(
                "domain",
                ""
            )
        ).lower()

        if not publisher:
            continue

        count = publisher_counts.get(
            publisher,
            0
        )

        if count >= max_per_publisher:
            continue

        publisher_counts[publisher] = (
            count + 1
        )

        diversified.append(
            result
        )

    return diversified

def rank_sources(results):

    ranked_results = []

    for result in results:

        url = result.get(
            "url",
            ""
        )

        category, score = classify_source(
            url
        )

        domain = get_domain(url)

        publisher_id = get_publisher_id(
            domain
        )

        ranked_result = {
            **result,
            "domain": domain,
            "publisher_id": publisher_id,
            "source_type": category,
            "source_score": score
        }

        ranked_results.append(
            ranked_result
        )

    ranked_results.sort(
        key=lambda item: item[
            "source_score"
        ],
        reverse=True
    )

    ranked_results = apply_domain_diversity(
       ranked_results,
       max_per_publisher=1
    )

    return ranked_results
