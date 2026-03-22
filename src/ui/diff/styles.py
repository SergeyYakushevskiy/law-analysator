from PyQt6.QtGui import QColor

COLORS = {
    "insert_bg": QColor(144, 238, 144),
    "delete_bg": QColor(255, 160, 122),
    "modify_bg": QColor(255, 255, 150),
    "delete_text": QColor(160, 0, 0),
    "insert_text": QColor(0, 96, 0),
}

STYLESHEET = """
QWidget {
    background-color: #ffffff;
    color: #000000;
    font-family: "Consolas", "Monaco", "Courier New", monospace;
    font-size: 12px;
}
QPlainTextEdit {
    border: 1px solid #cccccc;
    background-color: #ffffff;
    padding: 5px;
}
QLabel {
    font-weight: bold;
    padding: 5px;
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    border-bottom: none;
}
QScrollBar:vertical {
    width: 12px;
    background: #f0f0f0;
}
QScrollBar::handle:vertical {
    background: #cccccc;
    border-radius: 6px;
}
"""