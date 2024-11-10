import re
from typing import List


def regular_expression(query: str, candidates: List[str]) -> List[str]:
    clear_candidates: List[str] = []

    for candidate in candidates:
        is_best_result: bool = bool(
            re.match(rf"^(.*\s){query}(\s.*)?$", candidate, re.IGNORECASE)
        )

        if is_best_result:
            clear_candidates.append(candidate)

    return clear_candidates
