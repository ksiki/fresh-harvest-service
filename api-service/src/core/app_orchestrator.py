import logging

from scripts.db_seeder import DatabaseSeeder
from scripts.infrastructure_init import InfrastructureInitializer

from shared.common_config import settings
from shared.db.core.db_s3 import database as db_s3
from shared.db.core.db_sql import database as db_sql

logger = logging.getLogger(__name__)


class AppOrchestrator:
    def __init__(self):
        pass

    async def setup(self) -> None:
        logger.info("Begin setup app.")

        async with db_s3.session_dependency() as s3_session:
            await InfrastructureInitializer.run_bootstrap(
                s3_session=s3_session, bucket_name=settings.s3_bucket_name
            )
        async with (
            db_sql.session_dependency() as sql_session,
            db_s3.session_dependency() as s3_session,
        ):
            await DatabaseSeeder.run_bootstrap(
                sql_session=sql_session, s3_session=s3_session
            )

        logger.info("App setup completed successfully.")

    async def shutdown(self) -> None:
        await db_sql.dispose()
