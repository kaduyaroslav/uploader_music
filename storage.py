import json
from pathlib import Path
import asyncio


_lock = asyncio.Lock()


BASE_DIR = Path(__file__).resolve().parent
MUSIC_DIR = BASE_DIR / "music"
LOG_FILE = BASE_DIR / "Conversations.json"
AUDIO_EXTENSIONS = {".mp3", ".m4a"}


def load_file():
    if not LOG_FILE.exists():
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"[storage]{LOG_FILE} поврежден, начинаю с пустой базы")
        return []

def save_files(data):
    tmp = LOG_FILE.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    tmp.replace(LOG_FILE)


async def register_file(file_name, on_new):
    async with _lock:
        existing = load_file()
        if file_name in existing:
            return False

        await on_new()

        existing.append(file_name)
        save_files(existing)
        return True


def sync_from_disk():
    if not MUSIC_DIR.exists():
        return
    existing = load_file()
    existing_set = set(existing)
    befor = len(existing)

    for x in MUSIC_DIR.iterdir():
        if x.suffix in AUDIO_EXTENSIONS and x.name not in existing_set:
            existing.append(x.name)
            existing_set.add(x.name)

    if len (existing) != befor:
        save_files(existing)
        print(f"[storage] sync: +{len(existing) - befor}")
# files  = list(p.glob("*.mp3"))
