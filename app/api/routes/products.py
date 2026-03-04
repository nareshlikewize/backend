
from fastapi import APIRouter, HTTPException
from ...services.store import PRODUCTS, generate_snapshot

router = APIRouter(prefix='/products', tags=['products'])

@router.get('')
def list_products():
    return list(PRODUCTS.values())

@router.get('/{protect_product_id}')
def get_product(protect_product_id: str):
    item = PRODUCTS.get(protect_product_id)
    if not item:
        raise HTTPException(404, 'Product not found')
    return item

@router.put('')
def upsert_product(body: dict):
    if 'protect_product_id' not in body:
        raise HTTPException(400, 'protect_product_id is required')
    PRODUCTS[body['protect_product_id']] = body
    # generate snapshot
    snap = generate_snapshot(body['protect_product_id'])
    return { 'ok': True, 'snapshot_id': snap['protect_product_snapshot_id'] }
