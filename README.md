
# Oasis Admin Backend (Static / In-Memory)

**No databases required** — all data lives in memory. Perfect for local demos or when you have connectivity issues.

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

## Endpoints
- `GET /products` — list seeded + created products
- `GET /products/{protect_product_id}` — get product
- `PUT /products` — upsert product **(auto-creates snapshot)**
- `GET /contracts/{protect_product_id}` — list contracts for product
- `PUT /contracts` — upsert contract **(auto-creates snapshot)**
- `GET /features/{protect_product_id}` — list features
- `PUT /features` — upsert feature
- `GET /snapshots/{protect_product_id}` — list in-memory snapshots
- `GET /users` / `POST /users` / `GET /users/roles`

## Notes
- Memory resets on server restart.
- Snapshot generation mirrors your spec: new snapshot is created when a product or contract is updated.
- Seeded with your **GoldServicePlan** sample so the UI has data instantly.
```
protect_product_id = F6551D67-9CD2-4F09-9BD4-BAD28E33C945
```
