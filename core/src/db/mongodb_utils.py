import logging

from motor.motor_asyncio import AsyncIOMotorClient

from ..core.config import settings
from .mongodb import db


async def open_mongo_connection():
    print("⚡ [DEBUG] open_mongo_connection() is running!")
    logging.info("Connecting to Mongo...")

    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
        minPoolSize=settings.MIN_CONNECTIONS_COUNT,
    )

    try:
        await db.client.admin.command("ping")
        logging.info("✅ Connected to MongoDB successfully!")
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        logging.error(f"❌ Failed to connect to MongoDB: {e}")
        print(f"❌ Failed to connect to MongoDB: {e}")


async def close_mongo_connection():
    print("⚡ [DEBUG] close_mongo_connection() is running!")
    logging.info("Closing Mongo connection...")
    db.client.close()
    logging.info("Mongo connection closed!")
