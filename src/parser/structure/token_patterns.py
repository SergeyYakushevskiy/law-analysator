import re


SECTION_PATTERN = re.compile(
    r"^раздел\s+([IVXLC]+|\d+)",
    re.IGNORECASE
)

CHAPTER_PATTERN = re.compile(
    r"^глава\s+(\d+)",
    re.IGNORECASE
)

ARTICLE_PATTERN = re.compile(
    r"^статья\s+(\d+(\.\d+)?)",
    re.IGNORECASE
)

POINT_PATTERN = re.compile(
    r"^(\d+)\."
)

SUBPOINT_PATTERN = re.compile(
    r"^([а-яa-z])\)"
)