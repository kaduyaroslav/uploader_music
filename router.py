import asyncio
from pathlib import Path
from aiogram import  Router, F, Bot
from aiogram.types import Message
from storage import MUSIC_DIR, register_file
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import Command
from oiov import load_env
from aiogram.types import FSInputFile
from asyncio import sleep, create_task

router = Router()
pending_timers = {}


@router.message(F.audio)
async def process_audio(message: Message, bot: Bot ):
    user_id = message.from_user.id
    chat_id = message.chat.id
    file_id = message.audio.file_id
    file_name = Path(message.audio.file_name or f"{file_id}.mp3").name
    MUSIC_DIR.mkdir(exist_ok=True)


    async def say_thank():
        try:
            await sleep(90)
            await bot.send_message(chat_id=chat_id, text="Thank you for using the bot!")
        finally:
            if pending_timers.get(user_id) is asyncio.current_task():
                pending_timers.pop(user_id, None)


    async def download():
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, destination=MUSIC_DIR / file_name)


    await register_file(file_name, download)

    old = pending_timers.get(user_id)
    if old:
        old.cancel()

    pending_timers[user_id] = create_task(say_thank())



@router.message(Command("upload"))
async def upload_music(message, bot):
    for x in MUSIC_DIR.iterdir():
        file = FSInputFile(x)
        try:
            await bot.send_document(chat_id=load_env("id"), document=file)
        except TelegramRetryAfter as e:
            await sleep(e.retry_after)
            await bot.send_document(chat_id=load_env("id"), document=file)
