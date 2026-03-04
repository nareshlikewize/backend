
from fastapi import APIRouter
from ...repositories import dynamo

router = APIRouter(prefix='/snapshots', tags=['snapshots'])

@router.get('/{protect_product_id}')
def list_snapshots(protect_product_id: str):
    return dynamo.list_snapshots(protect_product_id)
