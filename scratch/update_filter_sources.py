with open("evidence/evidence_engine.py", "r", encoding="utf-8") as f:
    content = f.read()

old_filter = '''def filter_sources(
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
    ]'''

new_filter = '''def filter_sources(
    results,
    source_scope
):
    if not results:
        return []

    if source_scope == "Trusted news + official sources":
        allowed = {"official", "trusted news", "fact check", "web source"}
    elif source_scope == "News sources only":
        allowed = {"trusted news", "fact check"}
    elif source_scope == "Official sources only":
        allowed = {"official"}
    else:
        return results

    filtered = [
        result
        for result in results
        if str(result.get("source_type", "")).lower() in allowed
    ]
    if not filtered:
        return results
    return filtered'''

content = content.replace(old_filter, new_filter)

with open("evidence/evidence_engine.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated filter_sources in evidence/evidence_engine.py")

