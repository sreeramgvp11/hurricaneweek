# Hurricane Week Backend (Sprint 1 + Sprint 2)

## Local setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Copy env file from repo root:

```bash
cp ../.env.example .env
```

## Run API

```bash
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest -q
```

## Implemented endpoints

- `GET /api/health`
- `POST /api/simulations`
- `GET /api/simulations/{simulation_id}/event`
- `POST /api/simulations/{simulation_id}/decisions`
- `GET /api/simulations/{simulation_id}/explanation`
- `GET /api/simulations/{simulation_id}/report`
- `GET /api/simulations/{simulation_id}/timeline`

## Tiger Data telemetry

Set `DATABASE_URL` in `.env` to your Tiger Cloud/Timescale Postgres connection string. Every valid decision writes one telemetry row to `simulation_telemetry`, and `GET /api/simulations/{simulation_id}/timeline` reads those persisted rows back in timestamp order.

## Gemini explanations

Set `GEMINI_API_KEY` in `.env`. The simulation engine remains deterministic truth, Tiger Data remains persisted history, and Gemini only provides concise explanations for decisions, current simulation state, and the final report.

## Security checklist (secrets)

- Keep real credentials only in local `backend/.env`.
- Never commit `backend/.env` or any file containing live keys/passwords.
- Use `.env.example` placeholders only.
- Rotate credentials immediately if exposed.

### Optional secret scanning before push

```bash
pip install pre-commit detect-secrets
pre-commit install
pre-commit run --all-files
```
