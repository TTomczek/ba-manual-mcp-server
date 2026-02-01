import re
from functools import wraps
from typing import Any

SECRET_KEYWORDS = [
    "password", "passwd", "pwd", "secret", "token", "apikey", "api_key", "api-key", "accessToken", "access_token", "access-token", "authorization"
]

def _mask_secrets_in_str(s: str) -> str:
    # Maskiert "key: value" oder "key = value" sowie quoted "key": "value"
    keywords_pattern = '|'.join(map(re.escape, SECRET_KEYWORDS))

    # key: "value" or key = value  (unquoted key)
    pattern1 = rf'(\b(?:{keywords_pattern})\b)\s*[:=]\s*(".*?"|\'.*?\'|[^\s,;]+)'
    s = re.sub(
        pattern1,
        lambda m: f"{m.group(1)}: ****",
        s,
        flags=re.IGNORECASE
    )

    # quoted or unquoted JSON-like key: "value"
    # group(1) = optional surrounding quote char (or empty), group(2) = key
    pattern2 = rf'(["\']?)(\b(?:{keywords_pattern})\b)\1\s*:\s*(".*?"|\'.*?\'|[^\s,;]+)'
    s = re.sub(
        pattern2,
        lambda m: f'{m.group(1)}{m.group(2)}{m.group(1)}: ****',
        s,
        flags=re.IGNORECASE
    )

    return s

def _escape_quotation_marks_and_ticks(s: str) -> str:
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    s = s.replace("`", "\\`")
    return s

def _remove_path_traversal(s: str) -> str:
    # Entfernt Pfad-Traversal in einfachen Fällen
    while "/../" in s:
        s = s.replace("/../", "/")
    while "\\..\\" in s:
        s = s.replace("\\..\\", "\\")

    while "../" in s:
        s = s.replace("../", "")

    # # Führende ../ oder ..\ entfernen (mehrfach möglich)
    # s = re.sub(r'^(?:\.\.[/\\])+', '', s)
    #
    # # Auch für wiederholte führende .. nach Slash
    # s = re.sub(r'/(?:(\.\.)(/|$))+', '/', s)
    # # Für Backslashes als Pfadtrenner Replacement als callable, um Template-Escapes zu vermeiden
    # s = re.sub(r'\\(?:(\.\.)(\\|$))+', lambda m: '\\', s)
    return s

def _sanitize_value(value: Any) -> Any:
    # Direkter Wert
    if isinstance(value, str):
        value_redacted = _mask_secrets_in_str(value)
        value_escaped = _escape_quotation_marks_and_ticks(value_redacted)
        value_stripped = _remove_path_traversal(value_escaped)
        return value_stripped

    # Dictionary rekursiv bereinigen
    if isinstance(value, dict):
        out = {}
        for k, val in value.items():
            out[k] = "****" if any(kw in k.lower() for kw in SECRET_KEYWORDS) and not isinstance(val, (dict, list, tuple)) else _sanitize_value(val)
        return out

    # Liste bereinigen
    if isinstance(value, list):
        return [_sanitize_value(x) for x in value]

    # Tupel bereinigen
    if isinstance(value, tuple):
        return tuple(_sanitize_value(x) for x in value)

    return value

def sanitize_output():

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return _sanitize_value(result)

        return wrapper
    return decorator
