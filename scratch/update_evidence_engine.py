with open("evidence/evidence_engine.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace collect_evidence function
start_marker = "def collect_evidence("
end_marker = "return selected"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx) + len(end_marker)

new_func = '''def collect_evidence(
    claim,
    max_results_per_query=5,
    max_evidence=8,
    deep=False,
    source_scope="Trusted news + official sources"
):
    if not claim:
        return []

    queries = [claim.strip()]
    if deep:
        queries.append(f"{claim.strip()} news fact check")

    all_results = []
    for query_index, query in enumerate(queries):
        try:
            results = search_web(query, max_results=max_results_per_query)
            for result in results:
                result["_query_index"] = query_index
                all_results.append(result)
            if len(all_results) >= 6 and not deep:
                break
        except Exception:
            continue

    all_results = remove_duplicate_results(all_results)
    ranked = rank_sources(all_results)
    ranked = filter_sources(ranked, source_scope)

    evidence = []
    for result in ranked:
        url = result.get("url", "")
        if not url:
            continue

        snippet = (result.get("title", "") + ". " + result.get("description", "")).strip()
        relevant_text = snippet

        if deep and len(snippet.split()) < 12:
            page_text = fetch_page_text(url)
            if page_text:
                extracted = extract_relevant_sentences(claim, page_text, max_sentences=4)
                if extracted:
                    relevant_text = extracted

        if not relevant_text:
            continue

        relevance = calculate_relevance(
            claim,
            relevant_text,
            result.get("title", ""),
            result.get("description", "")
        )

        if relevance < 0.02:
            continue

        source_score = float(result.get("source_score", 0))
        final_score = (relevance * 100 * 0.70) + (source_score * 0.30)

        evidence.append({
            "title": result.get("title", ""),
            "url": url,
            "domain": result.get("domain", ""),
            "publisher_id": result.get("publisher_id", result.get("domain", "")),
            "source_type": result.get("source_type", "Other"),
            "source_score": source_score,
            "relevance_score": round(relevance, 3),
            "final_score": round(final_score, 2),
            "description": result.get("description", ""),
            "evidence_text": relevant_text
        })

    evidence.sort(
        key=lambda item: (item.get("final_score", 0), item.get("relevance_score", 0)),
        reverse=True
    )

    selected = []
    publishers = set()
    for item in evidence:
        publisher = str(item.get("publisher_id", item.get("domain", ""))).lower()
        if publisher in publishers:
            continue
        publishers.add(publisher)
        selected.append(item)
        if len(selected) >= max_evidence:
            break

    return selected'''

updated = content[:start_idx] + new_func + content[end_idx:]

# Also update fetch_page_text timeout from 10 to 2
updated = updated.replace("timeout=10", "timeout=2")

with open("evidence/evidence_engine.py", "w", encoding="utf-8") as f:
    f.write(updated)

print("Updated evidence/evidence_engine.py successfully")

