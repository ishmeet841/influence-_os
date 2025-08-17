
# Deployment Guide
- Docker: `docker compose up --build` after copying env examples.
- Render/Heroku: Deploy backend and frontend as separate services, set envs, expose ports 8000/3000.
- DB: For Postgres, set `SQLALCHEMY_DATABASE_URI` accordingly.
