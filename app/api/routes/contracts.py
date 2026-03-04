
from fastapi import APIRouter, HTTPException
from ...repositories import dynamo
from ...services.snapshot_service import generate_snapshot_for_product

router = APIRouter(prefix='/contracts', tags=['contracts'])

@router.get('/{protect_product_id}')
def list_contracts(protect_product_id: str):
    return dynamo.get_contracts(protect_product_id)

@router.put('')
def upsert_contract(body: dict):
    if 'protect_product_id' not in body or 'contract_type' not in body:
        raise HTTPException(400, 'protect_product_id and contract_type are required')
    dynamo.put_contract(body)
    # generate snapshot
    try:
        snap = generate_snapshot_for_product(body['protect_product_id'])
    except Exception as e:
        raise HTTPException(500, f'Snapshot generation failed: {e}')
    return { 'ok': True, 'snapshot_id': snap['protect_product_snapshot_id'] }
