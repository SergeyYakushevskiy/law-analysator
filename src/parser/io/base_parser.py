import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path

from src.parser.io.exceptions import ParserError

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    def parse(self, file_path: Path) -> str:
        logger.debug(f'парсинг файла: {file_path}')
        try:
            if not file_path.exists():
                raise ParserError(f'файл {file_path} не найден')

            raw_text = self._parse_file(file_path)
            norm_text = self._normalize_text(raw_text)

            logger.debug(f'файл {file_path} успешно считан')

            return norm_text
        except ParserError:
            raise
        except Exception as e:
            raise ParserError(f"ошибка считывания файла {file_path}: {e}") from e

    @abstractmethod
    def _parse_file(self, file_path: Path) -> str:
        pass

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.replace('\xa0', ' ').replace('\t', ' ').replace('\v', ' ')

        text = text.replace('\r', '')

        text = re.sub(r'([а-яА-ЯёЁ0-9])\s+\.(?=\s|$)', r'\1.', text)

        text = re.sub(r'([а-яА-ЯёЁ0-9])\s+\)', r'\1)', text)
        text = re.sub(r'\(\s+([а-яА-ЯёЁ0-9])', r'(\1', text)

        # Но частый кейс: "cт." (латинская c) -> "ст." (кириллическая с)
        text = re.sub(r'c\s*т\.', 'ст.', text, flags=re.IGNORECASE)

        text = re.sub(r'[ ]{2,}', ' ', text)

        lines = text.split('\n')
        normalized_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                normalized_lines.append(stripped)

        return '\n'.join(normalized_lines)