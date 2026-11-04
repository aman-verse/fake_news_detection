from ddgs import DDGS

def search_web(query, max_results=10):

    try:

        results = DDGS().text(
            query,
            region="in-en",
            safesearch="moderate",
            max_results=max_results
        )

    except Exception as error:

        raise RuntimeError(
            f"Web search failed: {error}"
        )

    formatted_results = []

    for result in results:

        formatted_results.append(
            {
                "title": result.get(
                    "title",
                    ""
                ),

                "url": result.get(
                    "href",
                    ""
                ),

                "description": result.get(
                    "body",
                    ""
                )
            }
        )

    return formatted_results
