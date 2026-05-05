from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from shared.db.repositories.users import UserRepository


@pytest.mark.asyncio
class TestUserRep:
    async def test_register_user_and_update_activity(self, user_rep: UserRepository):
        tg_id = 12345

        with patch("shared.db.repositories.users.func.now") as mock_now:
            start_time = datetime.now()
            mock_now.return_value = start_time

            user_id = await user_rep.register(tg_id=tg_id)

            future_time = start_time + timedelta(minutes=1)
            mock_now.return_value = future_time

            await user_rep.update_last_activity(tg_id=tg_id)

        user = await user_rep.get_by_id(id=user_id)
        assert user.last_activity == future_time
        assert user.last_activity > start_time

        id_after_reg = await user_rep.get_id_by_tg_id(tg_id=tg_id)
        assert id_after_reg == user_id
