import logging

from scripts.db_seeder import DatabaseSeeder
from scripts.infrastructure_init import InfrastructureInitializer

from shared.common_config import settings
from shared.db.core.db_s3 import database as s3_db
from shared.db.core.db_sql import database as sql_db

logger = logging.getLogger(__name__)


class AppOrchestrator:
    async def setup(self) -> None:
        logger.info("Begin setup app.")

        async with (
            sql_db.session_scope() as sql_session,
            s3_db.session_scope() as s3_session,
        ):
            await InfrastructureInitializer.run_bootstrap(
                s3_session=s3_session, bucket_name=settings.s3_bucket_name
            )
            await DatabaseSeeder.run_bootstrap(
                sql_session=sql_session, s3_session=s3_session
            )

        logger.info("App setup completed successfully.")

    async def shutdown(self) -> None:
        await sql_db.dispose()
