import re
import requests

from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from evidence.query_builder import (
    build_search_queries
)

from evidence.web_search import (
    search_web
)

from evidence.source_ranker import (
    rank_sources
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}

def clean_page_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

def fetch_page_text(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup([
            "script",
            "style",
            "noscript",
            "nav",
            "footer",
            "header",
            "form",
            "aside"
        ]):

            element.decompose()

        return clean_page_text(
            soup.get_text(
                " ",
                strip=True
            )
        )

    except Exception:

        return ""

def split_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 5
    ]

def keyword_score(
    claim,
    sentence
):

    claim_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            claim.lower()
        )
    )

    sentence_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            sentence.lower()
        )
    )

    if not claim_words:

        return 0.0

    return (
        len(
            claim_words
            & sentence_words
        )
        / len(claim_words)
    )

def tfidf_score(
    claim,
    sentence
):

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform([
            claim,
            sentence
        ])

        return float(
            cosine_similarity(
                vectors[0:1],
                vectors[1:2]
            )[0][0]
        )

    except Exception:

        return 0.0

def numeric_score(
    claim,
    sentence
):

    claim_numbers = set(
        re.findall(
            r"\b\d+(?:\.\d+)?\b",
            claim
        )
    )

    sentence_numbers = set(
        re.findall(
            r"\b\d+(?:\.\d+)?\b",
            sentence
        )
    )

    if not claim_numbers:

        return 0.0

    if claim_numbers & sentence_numbers:

        return 1.0

    return 0.0

def direct_fact_score(
    claim,
    sentence
):

    claim_lower = claim.lower()
    sentence_lower = sentence.lower()

    phrase_groups = [

        [
            "freezes",
            "freezing point",
            "freeze"
        ],

        [
            "highest mountain",
            "highest point",
            "highest elevation",
            "above sea level"
        ],

        [
            "revolves around",
            "orbits the sun",
            "orbit around the sun"
        ],

        [
            "largest ocean",
            "smallest ocean"
        ],

        [
            "founded in",
            "established in"
        ],

        [
            "most populous",
            "population"
        ],

        [
            "south america",
            "nepal",
            "tibet",
            "asia"
        ]
    ]

    for group in phrase_groups:

        claim_has = any(
            phrase in claim_lower
            for phrase in group
        )

        sentence_has = any(
            phrase in sentence_lower
            for phrase in group
        )

        if claim_has and sentence_has:

            return 1.0

    return 0.0

def extract_relevant_sentences(
    claim,
    text,
    max_sentences=6
):

    if not text:

        return ""

    sentences = split_sentences(
        text
    )

    if not sentences:

        return ""

    ranked = []

    for sentence in sentences:

        score = (
            keyword_score(
                claim,
                sentence
            ) * 0.35

            +

            tfidf_score(
                claim,
                sentence
            ) * 0.25

            +

            numeric_score(
                claim,
                sentence
            ) * 0.10

            +

            direct_fact_score(
                claim,
                sentence
            ) * 0.30
        )

        ranked.append(
            (
                sentence,
                score
            )
        )

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    selected = [
        sentence
        for sentence, score in ranked[
            :max_sentences
        ]
        if score >= 0.03
    ]

    return " ".join(
        selected
    )

def calculate_relevance(
    claim,
    evidence_text,
    title="",
    description=""
):

    if not claim or not evidence_text:

        return 0.0

    try:

        text = (
            title
            + " "
            + description
            + " "
            + evidence_text
        )

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform([
            claim,
            text
        ])

        return round(
            float(
                cosine_similarity(
                    vectors[0:1],
                    vectors[1:2]
                )[0][0]
            ),
            3
        )

    except Exception:

        return 0.0

def remove_duplicate_results(
    results
):

    unique = []

    seen_urls = set()
    seen_titles = set()

    for result in results:

        url = result.get(
            "url",
            ""
        ).strip()

        title = result.get(
            "title",
            ""
        ).strip()

        if not url:

            continue

        normalized_url = (
            url.lower().rstrip("/")
        )

        normalized_title = re.sub(
            r"\s+",
            " ",
            title.lower()
        ).strip()

        if normalized_url in seen_urls:

            continue

        if (
            normalized_title
            and normalized_title in seen_titles
        ):

            continue

        seen_urls.add(
            normalized_url
        )

        if normalized_title:

            seen_titles.add(
                normalized_title
            )

        unique.append(
            result
        )

    return unique

def filter_sources(
    results,
    source_scope
):

    if source_scope == (
        "Trusted news + official sources"
    ):

        allowed = {
            "official",
            "trusted news",
            "fact check"
        }

    elif source_scope == "News sources only":

        allowed = {
            "trusted news",
            "fact check"
        }

    elif source_scope == "Official sources only":

        allowed = {
            "official"
        }

    else:

        return results

    return [
        result
        for result in results
        if str(
            result.get(
                "source_type",
                ""
            )
        ).lower() in allowed
    ]

def add_targeted_queries(
    claim,
    queries
):

    lower = claim.lower()

    extra = []

    if (
        "water" in lower
        and "freez" in lower
    ):

        extra.extend([
            "water freezing point 0 Celsius NIST",
            "water freezes 0 C standard pressure NIST",
            "freezing point pure water 0 C official"
        ])

    if "everest" in lower:

        extra.extend([
            "Mount Everest highest altitude above sea level NOAA",
            "Mount Everest location Nepal Tibet official",
            "Mount Everest highest mountain Britannica"
        ])

    if "pacific ocean" in lower:

        extra.extend([
            "Pacific Ocean largest ocean NOAA",
            "Pacific Ocean largest ocean official",
            "Pacific Ocean smallest ocean false"
        ])

    if (
        "earth" in lower
        and (
            "sun" in lower
            or "solar system" in lower
        )
    ):

        extra.extend([
            "Earth revolves around Sun NASA",
            "Earth orbits Sun NASA",
            "Earth center solar system false NASA"
        ])

    if "united nations" in lower:

        extra.extend([
            "United Nations founded 1945 official",
            "United Nations established 1945 UN",
            "United Nations founded date Britannica"
        ])

    extra.extend([
        claim + " official",
        claim + " fact check"
    ])

    combined = queries + extra

    unique = []

    seen = set()

    for query in combined:

        normalized = (
            query.lower().strip()
        )

        if normalized in seen:

            continue

        seen.add(
            normalized
        )

        unique.append(
            query
        )

    return unique

def collect_evidence(
    claim,
    max_results_per_query=5,
    max_evidence=8,
    deep=False,
    source_scope=(
        "Trusted news + official sources"
    )
):

    if not claim:

        return []

    queries = build_search_queries(
        claim,
        deep=deep
    )

    queries = add_targeted_queries(
        claim,
        queries
    )

    all_results = []

    for query_index, query in enumerate(
        queries
    ):

        try:

            results = search_web(
                query,
                max_results=max_results_per_query
            )

            for result in results:

                result["_query_index"] = (
                    query_index
                )

                all_results.append(
                    result
                )

        except Exception:

            continue

    all_results = remove_duplicate_results(
        all_results
    )

    ranked = rank_sources(
        all_results
    )

    ranked = filter_sources(
        ranked,
        source_scope
    )

    evidence = []

    for result in ranked:

        url = result.get(
            "url",
            ""
        )

        if not url:

            continue

        page_text = fetch_page_text(
            url
        )

        if not page_text:

            page_text = (
                result.get(
                    "title",
                    ""
                )
                + ". "
                + result.get(
                    "description",
                    ""
                )
            )

        relevant_text = (
            extract_relevant_sentences(
                claim,
                page_text,
                max_sentences=6
            )
        )

        if not relevant_text:

            continue

        relevance = calculate_relevance(
            claim,
            relevant_text,
            result.get(
                "title",
                ""
            ),
            result.get(
                "description",
                ""
            )
        )

        if relevance < 0.05:

            fallback_text = (
                result.get(
                    "title",
                    ""
                )
                + ". "
                + result.get(
                    "description",
                    ""
                )
            )

            fallback_relevance = (
                calculate_relevance(
                    claim,
                    fallback_text
                )
            )

            if fallback_relevance > relevance:

                relevant_text = fallback_text

                relevance = (
                    fallback_relevance
                )

        if relevance < 0.03:

            continue

        source_score = float(
            result.get(
                "source_score",
                0
            )
        )

        final_score = (
            relevance * 100 * 0.70
            +
            source_score * 0.30
        )

        evidence.append({

            "title": result.get(
                "title",
                ""
            ),

            "url": url,

            "domain": result.get(
                "domain",
                ""
            ),

            "publisher_id": result.get(
                "publisher_id",
                result.get(
                    "domain",
                    ""
                )
            ),

            "source_type": result.get(
                "source_type",
                "Other"
            ),

            "source_score": source_score,

            "relevance_score": round(
                relevance,
                3
            ),

            "final_score": round(
                final_score,
                2
            ),

            "description": result.get(
                "description",
                ""
            ),

            "evidence_text": relevant_text
        })

    evidence.sort(
        key=lambda item: (
            item.get(
                "final_score",
                0
            ),
            item.get(
                "relevance_score",
                0
            )
        ),
        reverse=True
    )

    selected = []

    publishers = set()

    for item in evidence:

        publisher = str(
            item.get(
                "publisher_id",
                item.get(
                    "domain",
                    ""
                )
            )
        ).lower()

        if publisher in publishers:

            continue

        publishers.add(
            publisher
        )

        selected.append(
            item
        )

        if len(selected) >= max_evidence:

            break

    return selected
