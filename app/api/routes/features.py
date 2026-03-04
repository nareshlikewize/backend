
from fastapi import APIRouter, HTTPException
from ...repositories import dynamo

router = APIRouter(prefix='/features', tags=['features'])

@router.get('/{protect_product_id}')
def list_features(protect_product_id: str):
    return dynamo.get_features_by_product(protect_product_id)

@router.put('')
def upsert_feature(body: dict):
    if 'protect_product_id' not in body or 'feature' not in body:
        raise HTTPException(400, 'protect_product_id and feature are required')
    # Accept device_sku list as either list or set
    if isinstance(body.get('device_sku'), list):
        body['device_sku'] = list(dict.fromkeys(body['device_sku']))
    dynamo.put_feature(body)
    return { 'ok': True }
