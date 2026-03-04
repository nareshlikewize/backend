
from typing import Any, Dict, List, Optional
import boto3
from boto3.dynamodb.conditions import Key
from ..config.settings import settings

_session = boto3.session.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)
_dynamo = _session.resource('dynamodb')

product_table = _dynamo.Table(settings.DDB_PRODUCT_TABLE)
contract_table = _dynamo.Table(settings.DDB_CONTRACT_TABLE)
features_table = _dynamo.Table(settings.DDB_FEATURES_TABLE)
snapshot_table = _dynamo.Table(settings.DDB_SNAPSHOT_TABLE)

# NOTE: This code assumes partition key is protect_product_id for all tables.
# If your schema differs, adjust KeyConditionExpression/index usage accordingly.

def get_product(protect_product_id: str) -> Optional[Dict[str, Any]]:
    resp = product_table.get_item(Key={'protect_product_id': protect_product_id})
    return resp.get('Item')

def put_product(item: Dict[str, Any]) -> None:
    product_table.put_item(Item=item)


def get_contracts(protect_product_id: str) -> List[Dict[str, Any]]:
    # If table design uses a different PK/SK, update this to query instead of scan
    resp = contract_table.scan(
        FilterExpression=Key('protect_product_id').eq(protect_product_id)
    )
    items = resp.get('Items', [])
    return items

def put_contract(item: Dict[str, Any]) -> None:
    contract_table.put_item(Item=item)


def get_features_by_product(protect_product_id: str) -> List[Dict[str, Any]]:
    resp = features_table.scan(
        FilterExpression=Key('protect_product_id').eq(protect_product_id)
    )
    return resp.get('Items', [])

def put_feature(item: Dict[str, Any]) -> None:
    features_table.put_item(Item=item)


def put_snapshot(item: Dict[str, Any]) -> None:
    snapshot_table.put_item(Item=item)


def list_snapshots(protect_product_id: str) -> List[Dict[str, Any]]:
    resp = snapshot_table.scan(
        FilterExpression=Key('protect_product_id').eq(protect_product_id)
    )
    return resp.get('Items', [])
