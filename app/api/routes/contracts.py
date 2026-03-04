
from fastapi import APIRouter, HTTPException
from ...services.store import CONTRACTS, generate_snapshot

router = APIRouter(prefix='/contracts', tags=['contracts'])

@router.get('/{protect_product_id}')
def list_contracts(protect_product_id: str):
    return [c for c in CONTRACTS if c.get('protect_product_id') == protect_product_id]

@router.put('')
def upsert_contract(body: dict):
    if 'protect_product_id' not in body or 'contract_type' not in body:
        raise HTTPException(400, 'protect_product_id and contract_type are required')
    # Upsert by (protect_product_id, contract_type)
    found = False
    for i, c in enumerate(CONTRACTS):
        if c.get('protect_product_id')==body['protect_product_id'] and c.get('contract_type')==body['contract_type']:
            CONTRACTS[i] = body
            found = True
            break
    if not found:
        CONTRACTS.append(body)
    snap = generate_snapshot(body['protect_product_id'])
    return { 'ok': True, 'snapshot_id': snap['protect_product_snapshot_id'] }
