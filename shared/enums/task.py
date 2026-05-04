import enum


class TaskType(enum.StrEnum):
    VALIDATE_POST = "validate_post"
    ARCHIVE_POSTS = "archive_posts"
    DELETE_POSTS = "delete_posts"
    CHECKING_USER_SUBSCRIPTIONS = "checking_user_subscriptions"
