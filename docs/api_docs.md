
# API Docs (MVP)

## POST /profile/ingest
Body: { name, headline, role, industry, interests[], voice }
Return: { profile }

## POST /trends/research
Body: { industry, role, keywords[]? }
Return: { trends: string[] }

## POST /content/ideas
Body: { topic, goals[], tone, call_to_action, hashtags_hint[], bullets }
Return: { ideas: string[] }

## POST /content/schedule
Body: { content, variant_b?, scheduled_at: ISO datetime }
Return: { scheduled: { id, scheduled_at } }

## GET /analytics/summary
Return: aggregate analytics

## POST /analytics/ingest
Body: { post_id, likes, comments, shares, impressions }
Return: { message }
