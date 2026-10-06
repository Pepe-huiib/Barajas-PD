"""
Almacenamiento simple en JSON (data/tickets.json).
Guarda los tickets abiertos para que sobrevivan a reinicios del bot.
"""
import json
import time
from pathlib import Path

FILE = Path("data/tickets.json")


def _load() -> dict:
    if not FILE.exists():
        return {}
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def _save(data: dict) -> None:
    FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_ticket(channel_id: int, user_id: int, type_key: str) -> None:
    data = _load()
    now = time.time()
    data[str(channel_id)] = {
        "user_id": user_id,
        "type": type_key,
        "created_at": now,
        "last_activity": now,
        "claimed_by": None,
    }
    _save(data)


def get_ticket(channel_id: int) -> dict | None:
    return _load().get(str(channel_id))


def update_ticket(channel_id: int, **fields) -> None:
    data = _load()
    if str(channel_id) in data:
        data[str(channel_id)].update(fields)
        _save(data)


def remove_ticket(channel_id: int) -> None:
    data = _load()
    if data.pop(str(channel_id), None) is not None:
        _save(data)


def all_tickets() -> dict:
    return _load()


def get_open_tickets_of_user(user_id: int) -> list[int]:
    """Devuelve los IDs de canal de los tickets abiertos de un usuario."""
    return [int(cid) for cid, t in _load().items() if t["user_id"] == user_id]
