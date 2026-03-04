
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    DDB_PRODUCT_TABLE = os.getenv('DDB_PRODUCT_TABLE')
    DDB_CONTRACT_TABLE = os.getenv('DDB_CONTRACT_TABLE')
    DDB_FEATURES_TABLE = os.getenv('DDB_FEATURES_TABLE')
    DDB_SNAPSHOT_TABLE = os.getenv('DDB_SNAPSHOT_TABLE')
    DATABASE_URL = os.getenv('DATABASE_URL')

settings = Settings()
