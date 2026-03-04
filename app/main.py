
from fastapi import FastAPI
from .api.routes import products, contracts, features, snapshots, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Oasis Admin Backend (Static/In-Memory)', version='0.0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(products.router)
app.include_router(contracts.router)
app.include_router(features.router)
app.include_router(snapshots.router)
app.include_router(users.router)

@app.get('/')
async def root():
    return { 'status': 'ok', 'mode': 'in-memory' }
