import re


class TextPreprocessor:

    def preprocess(self, text: str) -> list[str]:

        text = text.replace("\r\n", "\n")

        lines = [
            re.sub(r'\s+', ' ', line).strip()  # убираем лишние пробелы
            for line in text.split("\n")
            if line.strip()
        ]

        return lines
