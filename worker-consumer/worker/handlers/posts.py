import logging

from better_profanity import profanity
from sightengine.client import SightengineClient
from worker.config import settings

from shared.db.repositories.images import ImageRepository
from shared.db.repositories.posts import PostRepository
from shared.db.repositories.users import UserRepository
from shared.enums.image_category import ImageCategory
from shared.queue.tasks import notify_user

logger = logging.getLogger(__name__)
_sightengine_client = SightengineClient(
    settings.sightengine_api_user, settings.sightengine_api_secret
)
profanity.load_censor_words()


class PostHandler:
    @staticmethod
    async def archive_posts(post_rep: PostRepository) -> None:
        await post_rep.archivate_all_old_posts()

    @staticmethod
    async def delete_posts(post_rep: PostRepository, img_rep: ImageRepository) -> None:
        images = await post_rep.delete_all_old_posts()
        for img in images:
            await img_rep.delete(category=ImageCategory.POST, name=img)

    @staticmethod
    async def validate_posts(
        post_id: int,
        post_rep: PostRepository,
        user_rep: UserRepository,
        image_rep: ImageRepository,
    ) -> None:
        post = await post_rep.get_by_id(id=post_id)
        if not post:
            return

        async def notify_on_invalid(message: str) -> None:
            user = await user_rep.get_by_id(id=post.user_id)
            text = f"Ваш пост #{post.id} был удален. Причина: {message}"
            await post_rep.delete_by_id(id=post.id)
            await image_rep.delete(ImageCategory.POST, name=post.image_name)
            await notify_user.kiq(tg_id=user.tg_id, message=text)

        if profanity.contains_profanity(post.description):
            await notify_on_invalid(
                message="В описании продукта содержится ненормативная лексика"
            )
            return

        try:
            image_url = await image_rep.get_url(
                category=ImageCategory.POST, name=post.image_name
            )
            output = _sightengine_client.check(
                "nudity", "wad", "offensive", "gore"
            ).set_url(image_url)

            if output.get("status") == "success":
                if output["gore"]["prob"] > 0.5:
                    await notify_on_invalid(message="На фото обнаружена жесть/кровь")
                    return
                if output["nudity"]["raw"] > 0.5:
                    await notify_on_invalid(
                        message="На фото обнаружен неприемлемый контент"
                    )
                    return

            lifetime = post.disable_at - post.pub_at
            await post_rep.reactivate(post_id=post.id, lifetime=lifetime)
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            await notify_on_invalid(
                message="Приносим свои извинения - у нас возникли проблемы с проверкой вашего поста. Попробуйте позже или обратитесь в поддержку"
            )
