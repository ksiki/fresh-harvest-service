import logging
from contextlib import asynccontextmanager
from typing import Final

import aioboto3
from aiobotocore.client import AioBaseClient
from botocore.exceptions import BotoCoreError, ClientError
from core.config import settings

logger = logging.getLogger(__name__)


class S3Client:
    __slots__ = ("_config", "_session")

    def __init__(self, endpoint_url: str, access_key: str, secret_key: str) -> None:
        self._config = {
            "endpoint_url": endpoint_url,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        self._session = aioboto3.Session()

    @asynccontextmanager
    async def session_dependency(self) -> AioBaseClient:
        try:
            async with self._session.client("s3", **self._config) as client:
                logger.info("S3 session created successfully")
                yield client
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Failed to create S3 session or connection error: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in S3 session lifecycle: {e}")
            raise
        finally:
            logger.info("S3 session context closed")


database: Final[S3Client] = S3Client(
    endpoint_url=settings.s3_endpoint_url,
    access_key=settings.s3_access_key,
    secret_key=settings.s3_secret_key,
)
