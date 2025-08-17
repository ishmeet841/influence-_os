
from sqlalchemy.orm import Session
from ..models import Analytics, ScheduledPost

class AnalyticsService:
    def __init__(self, settings, db: Session):
        self.settings = settings
        self.db = db

    def ingest(self, rec):
        row = Analytics(post_id=rec.post_id, likes=rec.likes, comments=rec.comments,
                        shares=rec.shares, impressions=rec.impressions)
        self.db.add(row); self.db.commit()

    def summary(self):
        # Aggregate simple totals and averages
        rows = self.db.query(Analytics).all()
        if not rows:
            return {"posts": 0, "total_likes": 0, "avg_engagement": 0.0}
        posts = len({r.post_id for r in rows})
        total_likes = sum(r.likes for r in rows)
        total_comments = sum(r.comments for r in rows)
        total_shares = sum(r.shares for r in rows)
        total_impr = sum(r.impressions for r in rows)
        avg_eng = (total_likes + total_comments*2 + total_shares*3) / max(total_impr, 1)
        return {
            "posts": posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "total_impressions": total_impr,
            "avg_engagement": round(avg_eng, 4),
        }
