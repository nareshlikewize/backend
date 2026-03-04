
from __future__ import annotations
from typing import Dict, Any, List
import uuid

# --- In-memory stores (no DB required) ---
PRODUCTS: Dict[str, Dict[str, Any]] = {}
CONTRACTS: List[Dict[str, Any]] = []
FEATURES: List[Dict[str, Any]] = []
SNAPSHOTS: List[Dict[str, Any]] = []
USERS: List[Dict[str, Any]] = [
    {"id": 1, "email": "admin@example.com", "name": "Admin", "is_active": True},
]
ROLES: List[Dict[str, Any]] = [
    {"id": 1, "name": "SuperAdmin"},
    {"id": 2, "name": "Viewer"},
]

# Seed with your sample product/contract/feature so UI has data immediately
SAMPLE_PRODUCT_ID = 'F6551D67-9CD2-4F09-9BD4-BAD28E33C945'
PRODUCTS[SAMPLE_PRODUCT_ID] = {
    "protect_product_id": SAMPLE_PRODUCT_ID,
    "account_id": "1D85871E-8AB9-4C97-B169-48140C8D586F",
    "name": "GoldServicePlan",
    "alias": "GoldServicePlan",
    "AccountProductStatusType": "Active",
    "is_active": True,
    "description": "Luxottica Gold service plan",
    "InsuranceDamagedCoverage": True
}

CONTRACTS.extend([
    {
        "contract_type": "Pricing",
        "protect_product_id": SAMPLE_PRODUCT_ID,
        "pricing": {
            "pricing": [
                {
                    "price_tier": {"make_model_list": "GoldServicePlanModels"},
                    "pricing_details": {"marketing_and_enrollment_fee_service": 50, "service_fee": 149.99}
                }
            ]
        }
    },
    {
        "contract_type": "ClaimLimit",
        "protect_product_id": SAMPLE_PRODUCT_ID,
        "claim_limit_type": "FixedClaimLimit",
        "claim_limit_varies_by_equiment_type": False,
        "claim_limit_info": {
            "claim_limit_info": [
                {"claim_limit": 2, "claim_types": ["Damaged"], "ignore_for_cle": False, "include_oem": False}
            ]
        }
    }
])

FEATURES.append({
    "feature": "Make_model_list",
    "protect_product_id": SAMPLE_PRODUCT_ID,
    "Name": "GoldServicePlanModels",
    "device_sku": ["assert1", "assert2"]
})

# Helper: build snapshot doc similar to earlier backend
import re

def snake(s: str) -> str:
    s = re.sub('(.)([A-Z][a-z]+)', r'_', s)
    s = re.sub('([a-z0-9])([A-Z])', r'_', s)
    return s.replace('__','_').lower()

def generate_snapshot(protect_product_id: str) -> Dict[str, Any]:
    product = PRODUCTS.get(protect_product_id)
    if not product:
        raise ValueError('Product not found')
    contracts = [c for c in CONTRACTS if c.get('protect_product_id') == protect_product_id]
    features = [f for f in FEATURES if f.get('protect_product_id') == protect_product_id]

    snap: Dict[str, Any] = {}
    for k in [
        'account_id','account_product_client_number','account_product_number','account_product_status_type',
        'activation_date','alias','description','is_active','is_locked','name','product_type','service_product_id',
        'insurance_product_type','insurance_underwriter_id','warranty_underwriter_id','underwriters','created_date_time','modified_date_time'
    ]:
        v = product.get(k) or product.get(k[0:1].upper()+k[1:])
        if v is None:
            parts = k.split('_')
            camel = parts[0] + ''.join(p.title() for p in parts[1:])
            v = product.get(camel)
        if v is not None:
            snap[k] = v
    snap['protect_product_id'] = protect_product_id
    snap['product_type'] = product.get('ProductType', product.get('product_type','Service'))

    claim = next((c for c in contracts if c.get('contract_type')=='ClaimLimit'), None)
    if claim:
        snap['claim_limit_type'] = claim.get('claim_limit_type')
        snap['claim_limit_varies_by_equiment_type'] = claim.get('claim_limit_varies_by_equiment_type', False)
        if 'claim_limit_info' in claim:
            snap['claim_limit_info'] = claim['claim_limit_info']

    pricing = next((c for c in contracts if c.get('contract_type')=='Pricing'), None)
    if pricing:
        inner = pricing.get('pricing', {})
        try:
            lst = inner.get('pricing', [])
            if lst:
                first = lst[0]
                price_tier = first.get('price_tier')
                pricing_details = first.get('pricing_details')
                snap['pricing'] = {
                    'price_tier': price_tier or {},
                    'pricing_details': pricing_details or {}
                }
        except Exception:
            pass

    covers = []
    if product.get('InsuranceDamagedCoverage') or product.get('insurance_damaged_coverage'):
        covers.append('Damaged')
    if covers:
        snap['insurance_coverage'] = { 'coverages': covers }

    mml = next((f for f in features if f.get('feature') in ['Make_model_list','MakeModelList','Make_model_List']), None)
    if mml:
        snap.setdefault('pricing', {})
        snap['pricing'].setdefault('price_tier', {})
        snap['pricing']['price_tier']['make_model_list'] = mml.get('Name') or mml.get('name')

    snap['protect_product_snapshot_id'] = str(uuid.uuid4())
    snap['snapshot_set'] = 1

    SNAPSHOTS.append(snap)
    return snap
