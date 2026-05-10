from typing import Annotated

from aiobotocore.client import AioBaseClient
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db.core.db_s3 import database as s3_db
from shared.db.core.db_sql import database as sql

SQLDatabaseSession = Annotated[AsyncSession, Depends(sql.session_dependency)]
S3DatabaseSession = Annotated[AioBaseClient, Depends(s3_db.session_dependency)]
