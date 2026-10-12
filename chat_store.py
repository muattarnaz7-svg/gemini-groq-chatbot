"""Simple JSON-file storage so chats survive app restarts."""
import json
import re
import uuid
from datetime import datetime
from pathlib import Path

CHATS_DIR = Path(__file__).parent / "chats"
_ID_RE = re.compile(r"^[a-f0-9]{12}$")


def new_chat_id() -> str:
    return uuid.uuid4().hex[:12]


def _path(chat_id: str) -> Path:
    if not _ID_RE.match(chat_id):
        raise ValueError("Invalid chat id")
    return CHATS_DIR / f"{chat_id}.json"


def _make_title(messages: list[dict[str, str]]) -> str:
    for m in messages:
        if m["role"] == "user":
            text = " ".join(m["content"].split())
            return text[:40] + ("…" if len(text) > 40 else "")
    return "New chat"


def save_chat(chat_id: str, messages: list[dict[str, str]]) -> None:
    CHATS_DIR.mkdir(exist_ok=True)
    path = _path(chat_id)
    now = datetime.now().isoformat(timespec="seconds")
    created = now
    if path.exists():
        try:
            created = json.loads(path.read_text(encoding="utf-8")).get("created", now)
        except (json.JSONDecodeError, OSError):
            pass
    data = {
        "id": chat_id,
        "title": _make_title(messages),
        "created": created,
        "updated": now,
        "messages": messages,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_chat(chat_id: str) -> dict | None:
    try:
        return json.loads(_path(chat_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def list_chats() -> list[dict]:
    """Return saved chats (id, title, updated), newest first."""
    if not CHATS_DIR.exists():
        return []
    chats = []
    for file in CHATS_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            chats.append(
                {
                    "id": data["id"],
                    "title": data.get("title", "Untitled"),
                    "updated": data.get("updated", ""),
                }
            )
        except (OSError, ValueError, KeyError):
            continue
    return sorted(chats, key=lambda c: c["updated"], reverse=True)


def delete_chat(chat_id: str) -> None:
    try:
        _path(chat_id).unlink()
    except (OSError, ValueError):
        pass
