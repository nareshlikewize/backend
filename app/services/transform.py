
import uuid
from typing import Dict, Any, List

# Helper: convert keys to snake_case if needed
import re

def snake(s: str) -> str:
    s = re.sub('(.)([A-Z][a-z]+)', r'_', s)
    s = re.sub('([a-z0-9])([A-Z])', r'_', s)
    return s.replace('__','_').lower()


def to_snapshot(product: Dict[str, Any], contracts: List[Dict[str, Any]], features: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Start with selected fields from product, transformed to snapshot schema
    snap: Dict[str, Any] = {}
    # copy common fields
    for k in [
        'account_id','account_product_client_number','account_product_number','account_product_status_type',
        'activation_date','alias','description','is_active','is_locked','name','product_type','service_product_id',
        'insurance_product_type','insurance_underwriter_id','warranty_underwriter_id','underwriters','created_date_time','modified_date_time'
    ]:
        # allow both camelCase/PascalCase versions by fallback
        v = product.get(k)
        if v is None:
            v = product.get(k[0].upper()+k[1:])
        if v is None:
            # try camelCase
            parts = k.split('_')
            camel = parts[0] + ''.join(p.title() for p in parts[1:])
            v = product.get(camel)
        if v is not None:
            snap[k] = v
    snap['protect_product_id'] = product['protect_product_id']
    snap['product_type'] = product.get('ProductType', product.get('product_type','Service'))

    # Claim limits contract
    claim_contract = next((c for c in contracts if c.get('contract_type')=='ClaimLimit'), None)
    if claim_contract:
        snap['claim_limit_type'] = claim_contract.get('claim_limit_type')
        snap['claim_limit_varies_by_equiment_type'] = claim_contract.get('claim_limit_varies_by_equiment_type', False)
        if 'claim_limit_info' in claim_contract:
            snap['claim_limit_info'] = claim_contract['claim_limit_info']

    # Pricing contract (flatten selected fields into pricing)
    pricing_contract = next((c for c in contracts if c.get('contract_type')=='Pricing'), None)
    if pricing_contract:
        pricing = pricing_contract.get('pricing', {})
        # The snapshot example expects pricing.price_tier.make_model_list and pricing.pricing_details
        if pricing and isinstance(pricing, dict):
            # Try to simplify if nested { pricing: { pricing: [..] } } to just first element
            try:
                lst = pricing.get('pricing',{}).get('pricing',[])
                if lst:
                    first = lst[0]
                    price_tier = first.get('price_tier') or first.get('priceTier')
                    pricing_details = first.get('pricing_details') or first.get('pricingDetails')
                    snap['pricing'] = {
                        'price_tier': price_tier or {},
                        'pricing_details': pricing_details or {}
                    }
            except Exception:
                pass

    # Insurance coverages (from product boolean flags -> list)
    covers = []
    mapping = [
        ('InsuranceDamagedCoverage','Damaged'),
    ]
    for pk, label in mapping:
        val = product.get(pk) or product.get(snake(pk))
        if val:
            covers.append(label)
    if covers:
        snap['insurance_coverage'] = { 'coverages': covers }

    # Grace and filing wait period example (copy if present)
    for field in ['filing_wait_period','grace_period']:
        if field in product:
            snap[field] = product[field]
        else:
            # attempt to reconstruct from individual fields (FilingWaitPeriodNew/Refurbished/Used)
            if field=='filing_wait_period':
                items=[]
                for ct, key in [('New','FilingWaitPeriodNew'),('Refurbished','FilingWaitPeriodRefurbished'),('Used','FilingWaitPeriodUsed')]:
                    val = product.get(key) or product.get(snake(key))
                    if val is not None:
                        items.append({'condition_type': ct, 'wait_period': int(val)})
                if items:
                    snap['filing_wait_period']={'filing_wait_period': items}
            if field=='grace_period':
                items=[]
                for ct, key in [('New','GracePeriodNew'),('Refurbished','GracePeriodRefurbished'),('Used','GracePeriodUsed')]:
                    val = product.get(key) or product.get(snake(key))
                    if val is not None:
                        items.append({'condition_type': ct, 'grace_period': int(val)})
                if items:
                    snap['grace_period']={'grace_period': items}

    # Attach make/model feature name if present
    mml = next((f for f in features if f.get('feature') in ['Make_model_list','MakeModelList','Make_model_List']), None)
    if mml:
        # Ensure pricing.price_tier exists
        snap.setdefault('pricing', {})
        snap['pricing'].setdefault('price_tier', {})
        snap['pricing']['price_tier']['make_model_list'] = mml.get('Name') or mml.get('name')

    # Required keys
    snap['protect_product_snapshot_id'] = str(uuid.uuid4())
    snap['snapshot_set'] = 1

    return snap
