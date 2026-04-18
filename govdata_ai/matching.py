from __future__ import annotations
from rapidfuzz import fuzz
from jellyfish import soundex, metaphone


class NameMatcher:
    """
    Smart name matching engine for government database records.

    Handles: typos, maiden names, middle names, nicknames, abbreviated names.
    Uses fuzzy + phonetic matching combined into a single confidence score.
    """

    def match(self, query: str, candidate: str) -> float:
        """
        Returns a 0.0–1.0 confidence score for how well two names match.

        Combines:
        - Token sort ratio (handles word order differences)
        - Partial ratio (handles abbreviated names)
        - Phonetic similarity (handles pronunciation variants)
        """
        q = query.strip().upper()
        c = candidate.strip().upper()

        if q == c:
            return 1.0

        # Fuzzy scores (0–100 scale from rapidfuzz)
        token_sort = fuzz.token_sort_ratio(q, c) / 100
        partial = fuzz.partial_ratio(q, c) / 100
        token_set = fuzz.token_set_ratio(q, c) / 100

        fuzzy_score = max(token_sort, partial, token_set)

        # Phonetic score — handles "Smith" vs "Smyth", "John" vs "Jon"
        phonetic_score = self._phonetic_similarity(q, c)

        # Weighted combination
        return round(0.7 * fuzzy_score + 0.3 * phonetic_score, 4)

    def phonetic_match(self, name1: str, name2: str, threshold: float = 0.8) -> bool:
        """Returns True if two names sound similar enough."""
        return self._phonetic_similarity(name1.upper(), name2.upper()) >= threshold

    def match_with_address(
        self,
        name: str,
        address: str,
        candidate_name: str,
        candidate_address: str,
    ) -> float:
        """
        Higher-confidence matching when address context is available.
        Address match boosts the overall score.
        """
        name_score = self.match(name, candidate_name)
        address_score = self._address_similarity(address, candidate_address)

        # If name is weak but address is strong, boost it
        return round(0.6 * name_score + 0.4 * address_score, 4)

    def _phonetic_similarity(self, a: str, b: str) -> float:
        """Compare phonetic codes of each word in the names."""
        words_a = a.split()
        words_b = b.split()

        if not words_a or not words_b:
            return 0.0

        scores = []
        for wa in words_a:
            for wb in words_b:
                try:
                    # Soundex: same code = exact phonetic match
                    sx_match = 1.0 if soundex(wa) == soundex(wb) else 0.0
                    # Metaphone: handles more complex cases
                    mp_match = 1.0 if metaphone(wa) == metaphone(wb) else 0.0
                    scores.append(max(sx_match, mp_match))
                except Exception:
                    scores.append(0.0)

        return max(scores) if scores else 0.0

    def _address_similarity(self, addr1: str, addr2: str) -> float:
        """Rough address similarity using token matching."""
        # Normalize
        a1 = addr1.upper().replace(",", " ").replace(".", "")
        a2 = addr2.upper().replace(",", " ").replace(".", "")
        return fuzz.token_set_ratio(a1, a2) / 100
