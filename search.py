import re
from typing import List, Dict

def format_timestamp(seconds: float) -> str:
    """
    Formats seconds as H:MM:SS
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}"

def search_transcript(
    segments: List[Dict[str, float]],
    words: List[str],
    context_window: int = 5
) -> List[Dict[str, object]]:
    """
    Searches the list of word-level segments for exact, case-insensitive matches,
    ignoring punctuation, and simple morphological variants (e.g., plural 's',
    suffix 'y', 'ish').

    Args:
        segments: List of dicts with 'start', 'end', 'text' keys.
        words: List of words to search for (case-insensitive exact match
               plus simple variants such as 's', 'y', 'ish').
        context_window: Number of words before and after to include in context.

    Returns:
        List of dicts, each with:
          - 'query': original search string (word or phrase)
          - 'timestamp_sec': float, start time in seconds of the match
          - 'timestamp': str, formatted timestamp H:MM:SS
          - 'context': str, words around the match
          - 'context_start_sec': float, start time in seconds of the context window
    """
    def _clean_token(token: str) -> str:
        return re.sub(r'[^0-9a-z]', '', token.lower())

    # Build phrase index: phrase_length -> {normalized_tuple: original_query}
    phrase_index: Dict[int, Dict[tuple, str]] = {}
    for query in words:
        raw_tokens = query.strip().split()
        cleaned = tuple(_clean_token(tok) for tok in raw_tokens)
        # Remove empty tokens
        cleaned = tuple(tok for tok in cleaned if tok)
        if not cleaned:
            continue
        length = len(cleaned)
        if length == 1:
            base = cleaned[0]
            variants = {base, f"{base}s", f"{base}y", f"{base}ish", f"{base}ing"}
            if base.endswith('e'):
                variants.add(f"{base[:-1]}ish")
            for var in variants:
                phrase_index.setdefault(1, {})[(var,)] = query
        else:
            phrase_index.setdefault(length, {})[cleaned] = query

    results = []
    total = len(segments)
    # Sort phrase lengths descending to match longer phrases first
    for i in range(total):
        for length in sorted(phrase_index.keys(), reverse=True):
            if i + length > total:
                continue
            segment_slice = segments[i:i + length]
            cleaned_slice = tuple(_clean_token(seg.get('text', '')) for seg in segment_slice)
            query_str = phrase_index[length].get(cleaned_slice)
            if query_str:
                start = segment_slice[0].get('start', 0.0)
                left = max(0, i - context_window)
                right = min(total - 1, i + length - 1 + context_window)
                context_words = [segments[j]['text'] for j in range(left, right + 1)]
                context_str = ' '.join(context_words)
                context_start = segments[left].get('start', 0.0)
                results.append({
                    'query': query_str,
                    'timestamp_sec': start,
                    'timestamp': format_timestamp(start),
                    'context': context_str,
                    'context_start_sec': context_start,
                })
                break
    return results