
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import ScheduledPost
from .linkedin import LinkedInService

_scheduler = None

def init_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.start()

def _job_post(scheduled_id: int, ls: LinkedInService, db: Session):
    rec = db.query(ScheduledPost).filter(ScheduledPost.id == scheduled_id).first()
    if not rec or rec.posted:
        return
    # pick A/B by simple coin flip on odd/even second
    content = rec.content if datetime.utcnow().second % 2 == 0 else (rec.variant_b or rec.content)
    ls.post(content)
    rec.posted = True
    db.commit()

def schedule_post(req, ls: LinkedInService, db: Session):
    rec = ScheduledPost(content=req.content, variant_b=req.variant_b or "", scheduled_at=req.scheduled_at)
    db.add(rec); db.commit(); db.refresh(rec)
    # For MVP, run immediately if time <= now
    if req.scheduled_at <= datetime.utcnow():
        _job_post(rec.id, ls, db)
    else:
        _scheduler.add_job(_job_post, 'date', run_date=req.scheduled_at, args=[rec.id, ls, db])
    return dict(id=rec.id, scheduled_at=rec.scheduled_at.isoformat())
