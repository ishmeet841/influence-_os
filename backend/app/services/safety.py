
import re

FORBIDDEN = [
    r"(?i)giveaway|lottery|crypto pump|work from home guaranteed income",
    r"(?i)hate speech|slur",  # placeholder
]

class SafetyService:
    def filter_text(self, txt: str) -> str:
        clean = txt.strip()
        # basic profanity/forbidden filters
        for pat in FORBIDDEN:
            clean = re.sub(pat, "[filtered]", clean, flags=re.IGNORECASE)
        # collapse excessive whitespace
        clean = re.sub(r"\n{3,}", "\n\n", clean)
        return clean
