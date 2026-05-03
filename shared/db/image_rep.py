import logging
from typing import Final

from aiobotocore.client import AioBaseClient

from shared.common_config import settings
from shared.db.core.base_rep import BaseRepository
from shared.enums.image_category import ImageCategory

logger = logging.getLogger(__name__)


class ImageRepository(BaseRepository[None, AioBaseClient]):
    BUCKET_NAME: Final[str] = settings.s3_bucket_name
    model = None

    async def get_by_id(self, id: int) -> None:
        """S3 репозиторий не реализовывает get_by_id, выбрасывается NotImplementedError"""
        raise NotImplementedError("S3 repository does not support get_by_id")

    async def get_url(self, category: ImageCategory, name: str) -> str:
        return await self._generate_presigned_url(f"{category}{name}")

    async def upload(self, category: ImageCategory, name: str, content: bytes) -> None:
        await self._upload_file(file_content=content, object_name=f"{category}{name}")

    async def delete(self, category: ImageCategory, name: str) -> None:
        await self._delete_file(object_name=f"{category}{name}")

    async def _generate_presigned_url(
        self, object_name: str, expiration: int = 3600
    ) -> str:
        return await self.session.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )

    async def _upload_file(
        self, file_content: bytes, object_name: str, content_type: str = "image/jpeg"
    ) -> None:
        try:
            await self.session.put_object(
                Bucket=self.BUCKET_NAME,
                Key=object_name,
                Body=file_content,
                ContentType=content_type,
            )
        except Exception as e:
            logger.error(f"S3 upload failed for {object_name}: {e}")
            raise

    async def _delete_file(self, object_name: str) -> None:
        try:
            await self.session.delete_object(Bucket=self.BUCKET_NAME, Key=object_name)
        except Exception as e:
            logger.error(f"S3 delete failed for {object_name}: {e}")
