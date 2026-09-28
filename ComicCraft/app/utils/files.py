import re, uuid

def safe_filename(value: str, max_length: int = 50) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_")
    return cleaned[:max_length] or "panel"

def unique_filename(prefix: str, suffix: str) -> str:
    return f"{safe_filename(prefix)}_{uuid.uuid4().hex[:10]}{suffix}"
