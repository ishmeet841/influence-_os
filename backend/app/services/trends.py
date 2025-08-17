
from typing import List
from ..settings import Settings

SEED_TRENDS = {
    "ai": [
        "Retrieval-augmented generation (RAG) in production",
        "Small language models (SLMs) on-device",
        "AI safety & evaluations becoming standard",
        "Agentic workflows for marketing ops",
        "Synthetic data for fine-tuning",
    ],
    "marketing": [
        "First-party data strategies post-cookies",
        "Short-form video + carousels outperforming long posts",
        "UGC + employee advocacy pipelines",
        "Marketing mix modeling (MMM) comeback",
    ],
}

class TrendService:
    def __init__(self, settings: Settings, db):
        self.settings = settings
        self.db = db

    def research(self, industry: str, role: str, keywords: List[str]) -> List[str]:
        key = industry.lower().strip()
        base = []
        if "ai" in key:
            base += SEED_TRENDS["ai"]
        if "market" in key or "growth" in key:
            base += SEED_TRENDS["marketing"]
        base += [f"Role-specific: {role} perspective on '{kw}'" for kw in (keywords or [])]
        # de-dup while preserving order
        seen, uniq = set(), []
        for t in base:
            if t not in seen:
                uniq.append(t); seen.add(t)
        return uniq[:10]
