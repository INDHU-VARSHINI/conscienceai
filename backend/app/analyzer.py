from typing import Dict, List, Tuple
import re

# --- Expanded, better-structured bias indicators ---
# Each entry is (list of low-severity phrases, list of high-severity phrases)
BIAS_PATTERNS = {
    "gender": (
        [
            r"\bguys\b",
            r"\bman up\b",
            r"\bwomens?\b",  # we will catch context later
            r"\bmoms?\b",
            r"\bmen are\b",
            r"\bwomen are\b",
            r"\b(?:he|she) should\b",
        ],
        [
            r"\b(women can't|women cannot|women can't)\b",
            r"\b(men are stronger|men always|women are weaker)\b",
            r"\b(?:she's|he's) emotional\b",
            r"\bonly (?:men|women)\b",
            r"\b(?:women|men) belong\b",
        ],
    ),
    "race": (
        [
            r"\bimmigrant(s)?\b",
            r"\bforeigners?\b",
            r"\bthey come here\b",
        ],
        [
            r"\b(ethnic slur|those people)\b",
            r"\b(black people are|white people are|asians are)\b",
            r"\binferior race\b",
            r"\bracist\b",
        ],
    ),
    "age": (
        [
            r"\bmillennial(s)?\b",
            r"\bboom(er|ers)?\b",
        ],
        [
            r"\bold people\b",
            r"\btoo old to\b",
            r"\btoo young to\b",
            r"\byoungsters are lazy\b",
        ],
    ),
    "religion": (
        [
            r"\bchristian(s)?\b",
            r"\bmuslim(s)?\b",
            r"\bhindu(s)?\b",
            r"\b(jew(s)?)\b",
        ],
        [
            r"\b(atheists can't be trusted|religious nut|infidel|holy war)\b",
            r"\bmuslims are\b",
            r"\bchristians are\b",
        ],
    ),
    "nationality": (
        [
            r"\bindians?\b",
            r"\bamericans?\b",
            r"\bchinese\b",
            r"\boutsiders\b",
        ],
        [
            r"\bimmigrants take jobs\b",
            r"\bthey come here and\b",
        ],
    ),
    "disability": (
        [
            r"\bdisabled people\b",
            r"\bmentally ill\b",
            r"\bhandicapped\b",
        ],
        [
            r"\b(retard(ed)?|crippled)\b",
            r"\b(insane|crazy)\b",
        ],
    ),
    "appearance": (
        [
            r"\bfat people\b",
            r"\bugly\b",
            r"\bdark skin\b",
            r"\bskinny\b",
        ],
        [
            r"\blooks weird\b",
            r"\btoo (?:tall|short)\b",
        ],
    ),
    "socioeconomic": (
        [
            r"\bpoor people\b",
            r"\brich people\b",
            r"\blower class\b",
        ],
        [
            r"\bpoor people are lazy\b",
            r"\brich people are greedy\b",
            r"\buneducated masses\b",
        ],
    ),
}

# replacements are used to produce a neutral suggestion
CORRECTIONS = {
    r"\bonly men\b": "people",
    r"\bguys\b": "people / folks / team",
    r"\bwomen can't\b": "anyone can",
    r"\bmen are stronger\b": "strength varies between individuals",
    r"\bold people\b": "older adults",
    r"\bpoor people are lazy\b": "people from different socioeconomic backgrounds can be hardworking",
    r"\bright people are greedy\b": "wealth does not determine character",
    r"\bfat people\b": "people of larger body size",
    r"\b(retard(ed)?|crippled)\b": "use respectful clinical or person-first language (e.g. 'person with a developmental disability')",
    r"\bimmigrants take jobs\b": "immigrants contribute to the workforce",
    r"\bguys\b": "people",
}

# severity weights
HIGH_SEVERITY_WEIGHT = 3
LOW_SEVERITY_WEIGHT = 1

def normalize_text(text: str) -> str:
    return text.lower()

def find_matches(text: str) -> Dict[str, List[Tuple[str, int]]]:
    normalized = normalize_text(text)
    results: Dict[str, List[Tuple[str, int]]] = {k: [] for k in BIAS_PATTERNS.keys()}

    for cat, (low_list, high_list) in BIAS_PATTERNS.items():
        for pattern in high_list:
            for m in re.finditer(pattern, normalized, flags=re.IGNORECASE):
                results[cat].append((m.group(0), HIGH_SEVERITY_WEIGHT))
        for pattern in low_list:
            for m in re.finditer(pattern, normalized, flags=re.IGNORECASE):
                results[cat].append((m.group(0), LOW_SEVERITY_WEIGHT))

        # detect phrases like "men are better than women"
        comp_pattern = r"\b([a-z]+)s?\s+are\s+(?:better|worse|less|more)\s+than\s+([a-z]+)s?\b"
        for m in re.finditer(comp_pattern, normalized, flags=re.IGNORECASE):
            subj, obj = m.group(1), m.group(2)
            if subj in ["men", "women", "girls", "boys"]:
                results["gender"].append((m.group(0), HIGH_SEVERITY_WEIGHT))
            elif subj in ["old", "young"]:
                results["age"].append((m.group(0), HIGH_SEVERITY_WEIGHT))
            elif subj in ["immigrant", "foreigner"]:
                results["nationality"].append((m.group(0), HIGH_SEVERITY_WEIGHT))

    return results

def mock_rate_bias(text: str) -> Dict[str, int]:
    """
    Score 1..5 for each category.
    Score is computed from the sum of weights found; then mapped to 1..5.
    """
    matches = find_matches(text)
    scores: Dict[str, int] = {}
    max_score = 1
    for cat, hits in matches.items():
        total_weight = sum(w for (_, w) in hits)
        # map weight to 1..5 (tune thresholds)
        if total_weight == 0:
            score = 1
        elif total_weight <= 2:
            score = 2
        elif total_weight <= 4:
            score = 3
        elif total_weight <= 7:
            score = 4
        else:
            score = 5
        scores[cat] = score
        max_score = max(max_score, score)
    scores["overall"] = max_score
    return scores

def mock_highlights(text: str, scores: Dict[str, int]) -> Dict[str, List[str]]:
    matches = find_matches(text)
    highlights: Dict[str, List[str]] = {}
    for cat, hits in matches.items():
        if hits:  # always show matches, not only when score>2
            unique = list({span for span, _ in hits})
            explanation = {
                "gender": "Gendered or stereotypical statement detected.",
                "race": "Possible racial or ethnic generalization.",
                "age": "Age-based stereotyping or exclusion.",
                "religion": "Negative or generalizing language about religion.",
                "nationality": "Xenophobic or nationality-based claim.",
                "disability": "Insensitive or derogatory mention of disabilities.",
                "appearance": "Body or appearance-based judgement.",
                "socioeconomic": "Stereotypes based on wealth or class."
            }.get(cat, "Potential bias detected.")
            highlights[cat] = [explanation] + unique
    return highlights

def generate_correction(text: str, scores: Dict[str, int]) -> str:
    """
    Replace detected biased phrases with neutral alternatives.
    Uses both predefined replacements and detected phrases.
    """
    matches = find_matches(text)
    corrected = text

    # iterate through all matches
    for cat, hits in matches.items():
        for phrase, weight in hits:
            # check if we have a replacement
            replacement = None
            for pattern, repl in CORRECTIONS.items():
                if re.fullmatch(pattern, phrase, flags=re.IGNORECASE):
                    replacement = repl
                    break
            if replacement:
                # replace all occurrences of this phrase (case-insensitive)
                corrected = re.sub(re.escape(phrase), replacement, corrected, flags=re.IGNORECASE)

    return corrected
