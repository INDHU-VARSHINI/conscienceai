def retrieve_sources(scores: dict):
    sources = []
    if scores.get("gender", 0) > 2:
        sources.append({
            "id": "G1",
            "title": "Use gender-neutral language",
            "content": "Guidance: Prefer gender-neutral terms (e.g., 'they', 'people', job titles without gender)."
        })
    if scores.get("race", 0) > 2:
        sources.append({
            "id": "R1",
            "title": "Avoid racial generalizations",
            "content": "Guidance: Avoid blanket statements that attribute traits to entire racial groups."
        })
    if scores.get("age", 0) > 2:
        sources.append({
            "id": "A1",
            "title": "Age-inclusive language",
            "content": "Guidance: Use person-first and neutral descriptions for age (e.g., 'older adults')."
        })
    # fallback
    if not sources:
        sources.append({
            "id": "S0",
            "title": "General bias avoidance",
            "content": "Guidance: Avoid stereotypes, focus on behavior or evidence rather than identity."
        })
    return sources
