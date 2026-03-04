
from fastapi import APIRouter, HTTPException
from ...services.store import FEATURES

router = APIRouter(prefix='/features', tags=['features'])

@router.get('/{protect_product_id}')
def list_features(protect_product_id: str):
    return [f for f in FEATURES if f.get('protect_product_id') == protect_product_id]

@router.put('')
def upsert_feature(body: dict):
    if 'protect_product_id' not in body or 'feature' not in body:
        raise HTTPException(400, 'protect_product_id and feature are required')
    # Upsert by (protect_product_id, feature)
    for i, f in enumerate(FEATURES):
        if f.get('protect_product_id')==body['protect_product_id'] and f.get('feature')==body['feature']:
            FEATURES[i] = body
            break
    else:
        FEATURES.append(body)
    return { 'ok': True }
