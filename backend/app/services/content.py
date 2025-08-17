
from typing import List
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from ..schemas import ProfileIn, PostIdeaRequest
from ..models import Profile, ScheduledPost
from ..settings import Settings
from .llm import LLMClient
from .prompts import IDEA_SYSTEM, IDEA_PROMPT, HASHTAG_SYSTEM, HASHTAG_PROMPT

class ContentService:
    def __init__(self, settings: Settings, db: Session):
        self.settings = settings
        self.db = db
        self.llm = LLMClient(settings)

    def save_profile(self, payload: ProfileIn) -> Profile:
        # single-profile MVP
        q = self.db.query(Profile).first()
        if not q:
            q = Profile(
                name=payload.name,
                headline=payload.headline,
                role=payload.role,
                industry=payload.industry,
                interests=",".join(payload.interests or []),
                voice=payload.voice
            )
            self.db.add(q)
        else:
            q.name = payload.name
            q.headline = payload.headline
            q.role = payload.role
            q.industry = payload.industry
            q.interests = ",".join(payload.interests or [])
            q.voice = payload.voice
        self.db.commit()
        self.db.refresh(q)
        return q

    def get_profile(self) -> Profile | None:
        return self.db.query(Profile).first()

    def _format_idea_prompt(self, req: PostIdeaRequest, profile: Profile) -> str:
        return IDEA_PROMPT.format(
            role=profile.role,
            industry=profile.industry,
            interests=profile.interests,
            tone=req.tone,
            goals=", ".join(req.goals or []),
            cta=req.call_to_action,
            bullets=req.bullets,
            n=5,
            topic=req.topic
        ) + f"\nTopic focus: {req.topic}\nVoice: {profile.voice}"

    def _format_hashtag_prompt(self, content: str) -> str:
        return HASHTAG_PROMPT.format(content=content)

    def _make_variant_b(self, content: str) -> str:
        # simple tweak: different hook style + CTA
        lines = content.splitlines()
        if lines:
            lines[0] = "Alt hook: " + lines[0].lstrip("- ")[:120]
        return "\n".join(lines) + "\n\n(Version B CTA) What would you do differently?"

    def generate_post_ideas(self, req: PostIdeaRequest) -> List[str]:
        profile = self.get_profile()
        if not profile:
            # minimal fallback
            fake = f"Idea: {req.topic} — bullet points and hashtags. CTA: {req.call_to_action}"
            return [fake]
        prompt = self._format_idea_prompt(req, profile)
        system = IDEA_SYSTEM
        # run sync for MVP by calling async via loop
        async def _go():
            return await self.llm.chat(system, prompt)
        ideas_text = asyncio.get_event_loop().run_until_complete(_go())
        # Split into ideas
        chunks = [c.strip() for c in ideas_text.split("\n\n") if len(c.strip())>0]
        return chunks[:5]
