
from typing import Dict, Any, List
from .transform import to_snapshot
from ..repositories import dynamo

def generate_snapshot_for_product(protect_product_id: str) -> Dict[str, Any]:
    product = dynamo.get_product(protect_product_id)
    if not product:
        raise ValueError('Product not found')
    contracts = dynamo.get_contracts(protect_product_id)
    features = dynamo.get_features_by_product(protect_product_id)
    snapshot_item = to_snapshot(product, contracts, features)
    dynamo.put_snapshot(snapshot_item)
    return snapshot_item
