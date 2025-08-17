
# Technical Report — Influence OS (MVP)

## Architecture
- **Frontend:** Next.js dashboard for profile management, idea generation, scheduling, and analytics.
- **Backend:** FastAPI with endpoints for profile ingest, trend research, content generation, scheduling, analytics.
- **Scheduler:** APScheduler triggers post jobs at scheduled times.
- **LLM:** Pluggable OpenAI-compatible client. Offline fallback returns deterministic strings for demo without API keys.
- **LinkedIn Adapter:** Mock by default; switch to real once OAuth credentials are added.
- **DB:** SQLite in dev, Postgres-ready via env variable.

## AI Model Choices
- Chat-completions model configured via `OPENAI_MODEL`. Prompt templates enforce tone, structure, and safety policy.

## Implementation Details
- A/B testing toggles content vs. variant B at posting time.
- Safety filter removes risky patterns and normalizes whitespace.
- Trend service returns seed trends deterministically, extendable to live search APIs.

## Future Enhancements
- OAuth2 flow for LinkedIn + token store.
- Live trend ingestion via vetted APIs.
- Image generation for carousels.
- Multi-user tenancy, RBAC.
