import enum


class PostStatus(enum.StrEnum):
    ACTIVE = "active"
    ARCHIVE = "archive"
    VALIDATE = "validate"
