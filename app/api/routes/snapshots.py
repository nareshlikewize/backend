
from fastapi import APIRouter
from ...services.store import SNAPSHOTS

router = APIRouter(prefix='/snapshots', tags=['snapshots'])

@router.get('/{protect_product_id}')
def list_snapshots(protect_product_id: str):
    return [s for s in SNAPSHOTS if s.get('protect_product_id') == protect_product_id]
