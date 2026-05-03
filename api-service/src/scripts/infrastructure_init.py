import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Final

from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class InfrastructureInitializer:
    ALEMBIC_INI_PATH: Final[Path] = (
        Path(__file__).resolve().parent.parent.parent / "alembic.ini"
    )

    def __init__(self, s3_session: AioBaseClient, bucket_name: str) -> None:
        self.s3_session = s3_session
        self.bucket_name = bucket_name

    @classmethod
    async def run_bootstrap(cls, s3_session: AioBaseClient, bucket_name: str) -> None:
        initializer = cls(s3_session=s3_session, bucket_name=bucket_name)
        await initializer.run_all()
        logger.info("Infrastructure initialization completed successfully.")

    async def run_all(self) -> None:
        await asyncio.to_thread(self._run_migrations)
        await self._init_s3()

    def _run_migrations(self):
        logger.info("Starting database migrations via Subprocess")
        try:
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"Alembic output: {result.stdout}")
            logger.info("Database migrations finished successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Alembic failed with error: {e.stderr}")
            raise e

    async def _init_s3(self):
        logger.info(f"Checking S3 bucket: {self.bucket_name}")
        try:
            await self.s3_session.head_bucket(Bucket=self.bucket_name)
            logger.info(f"S3 Bucket '{self.bucket_name}' exists.")
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code in ("404", "NoSuchBucket"):
                logger.info(f"Bucket '{self.bucket_name}' not found. Creating...")
                await self.s3_session.create_bucket(Bucket=self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created successfully.")
            else:
                logger.error(f"Unexpected S3 error: {e}")
                raise e
