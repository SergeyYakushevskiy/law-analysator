from src.config.paths import LOG_DIR

def ensure_directories():
    dirs = [
        LOG_DIR
    ]
    for dir in dirs:
        if not dir.exists():
            dir.mkdir(parents=True, exist_ok=True)
