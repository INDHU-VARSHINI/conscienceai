def retrieve_sources(scores):
    # return mock sources/guidelines relevant to the biases found
    sources = []
    if scores.get("gender",0)>2:
        sources.append({"id":"G1", "title":"Avoid gendered language", "content":"Prefer gender-neutral terms."})
    if scores.get("race",0)>2:
        sources.append({"id":"R1", "title":"Respectful racial descriptors", "content":"Avoid labels that generalize or demean."})
    if scores.get("age",0)>2:
        sources.append({"id":"A1", "title":"Age neutrality guidance", "content":"Do not generalize based on age."})
    return sources
