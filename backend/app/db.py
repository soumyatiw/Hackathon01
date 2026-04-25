import os
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from app.config import MONGODB_URI
import logging
import certifi

logger = logging.getLogger(__name__)

# Create client with certifi for SSL certificates and a timeout
client = AsyncIOMotorClient(
    MONGODB_URI, 
    serverSelectionTimeoutMS=5000,
    tlsCAFile=certifi.where()
)

# Get database name from URI or default to 'chatbot_db'
# Atlas URIs often have the db name after the last '/'
try:
    db_name = MONGODB_URI.split('/')[-1].split('?')[0] or "chatbot_db"
except Exception:
    db_name = "chatbot_db"

db = client[db_name]

async def get_db():
    try:
        # Verify connection
        await client.admin.command('ping')
        return db
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise e
