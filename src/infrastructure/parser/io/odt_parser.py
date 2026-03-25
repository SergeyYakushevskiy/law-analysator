import logging
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from src.infrastructure.parser.io.base_parser import BaseParser

logger = logging.getLogger(__name__)


class OdtParser(BaseParser):

    def _parse_file(self, file_path: Path) -> str:

        with zipfile.ZipFile(file_path) as odt:
            with odt.open("content.xml") as xml_file:
                tree = ET.parse(xml_file)

        root = tree.getroot()

        namespaces = {
            "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        }

        text_elements = []

        for tag in ("text:p", "text:h"):
            for element in root.findall(f".//{tag}", namespaces):
                text = "".join(element.itertext()).strip()
                if text:
                    text_elements.append(text)

        text = "\n".join(text_elements)

        return text
