import logging
from pathlib import Path

from src.infrastructure.config import ThemeMode

logger = logging.getLogger(__name__)

BASE_STYLE_FILE = "base.qss"
THEME_FILE_PATTERN = "theme_{theme}.qss"
COMPONENTS_DIR = "components"

class ThemeManager:
    def __init__(self, style_dir: Path):
        self.style_dir = style_dir

    def get_stylesheet(self, theme: ThemeMode) -> str:
        logger.debug(f"cборка темы: {theme}")
        parts = []

        base_file = self.style_dir / BASE_STYLE_FILE
        if base_file.exists():
            parts.append(base_file.read_text(encoding="utf-8"))
        else:
            logger.debug(f'файл {base_file} не найден')

        theme_file = self.style_dir / THEME_FILE_PATTERN.format(theme=theme)
        if theme_file.exists():
            parts.append(theme_file.read_text(encoding="utf-8"))
        else:
            logger.debug(f'файл {theme_file} не найден')

        components_dir = self.style_dir / COMPONENTS_DIR
        if components_dir.exists():
            for qss_file in sorted(components_dir.glob("*.qss")):
                parts.append(qss_file.read_text(encoding="utf-8"))

        result = "\n".join(parts)
        return result

    def switch_theme(self, app, new_theme: ThemeMode):
        stylesheet = self.get_stylesheet(new_theme)
        app.setStyleSheet(stylesheet)
        logger.debug(f'тема {new_theme} применена')