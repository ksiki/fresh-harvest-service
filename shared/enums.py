import enum


class PostStatus(enum.StrEnum):
    ACTIVE = "active"
    ARCHIVE = "archive"
    VALIDATE = "validate"


class ImageCategory(enum.StrEnum):
    PRODUCT = "product_icons/"
    POST = "post_image/"
