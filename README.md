# Uploader Music

A Telegram bot built with Python and [aiogram](https://docs.aiogram.dev/) that collects music files and forwards them to a chosen chat.

## What it does

- Accepts audio files (`.mp3`, `.m4a`) sent to the bot and saves them to the `music/` folder.
- Skips duplicates: the names of saved files are stored in a JSON file, so the same track is not downloaded twice.
- The `/upload` command sends all saved files to a separate chat.
- Handles Telegram flood limits (`TelegramRetryAfter`): waits and retries.
- Sends a thank-you message 90 seconds after the last uploaded file (the timer resets with every new file).

## Tech stack

- Python 3.10+
- aiogram 3 (async Telegram Bot framework)
- asyncio
- python-dotenv

## Project structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point, starts the bot (long polling) |
| `router.py` | Message handlers: audio upload and `/upload` command |
| `storage.py` | Saving files, duplicate check, JSON log with `asyncio.Lock` and safe writes |
| `config.py` | Loads settings from the `.env` file |
| `.env.example` | Example of environment variables |

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kaduyaroslav/uploader_music.git
   cd uploader_music
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install aiogram python-dotenv
   ```

3. Create a bot with [@BotFather](https://t.me/BotFather) and get its token.

4. Copy `.env.example` to `.env` and fill in the values:

   ```env
   Bot_token=your_bot_token
   Chat_id=id_of_the_chat_for_uploads
   ```

5. Run the bot:

   ```bash
   python main.py
   ```

## Usage

1. Send an audio file (mp3 or m4a) to the bot. It will be saved to `music/`.
2. Send `/upload` to forward all saved files to the chat from `Chat_id`.

## Possible improvements

- Handle the case when the `music/` folder does not exist yet in `/upload`
- Send only audio files (`.mp3`, `.m4a`) in `/upload`
- Add a `requirements.txt`
- Run the bot on a VPS with systemd or Docker

## Author

Yaroslav, self-taught Python developer. Telegram bots, MySQL, basic Linux and front-end.
