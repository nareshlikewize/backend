
from fastapi import APIRouter, HTTPException
from ...repositories import dynamo
from ...services.snapshot_service import generate_snapshot_for_product

router = APIRouter(prefix='/products', tags=['products'])

@router.get('')
def list_products():
    # For demo, we do a scan (in real systems, avoid scans)
    from boto3.dynamodb.conditions import Key
    resp = dynamo.product_table.scan()
    return resp.get('Items', [])

@router.get('/{protect_product_id}')
def get_product(protect_product_id: str):
    item = dynamo.get_product(protect_product_id)
    if not item:
        raise HTTPException(404, 'Product not found')
    return item

@router.put('')
def upsert_product(body: dict):
    if 'protect_product_id' not in body:
        raise HTTPException(400, 'protect_product_id is required')
    dynamo.put_product(body)
    # generate snapshot
    try:
        snap = generate_snapshot_for_product(body['protect_product_id'])
    except Exception as e:
        raise HTTPException(500, f'Snapshot generation failed: {e}')
    return { 'ok': True, 'snapshot_id': snap['protect_product_snapshot_id'] }
