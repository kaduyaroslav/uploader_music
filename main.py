import asyncio
from aiogram import Bot, Dispatcher
from router import router
from oiov import load_env

dp = Dispatcher()
dp.include_router(router)

async def main():
    # print(AID_Token)
    bot = Bot(token=load_env("token"))
    print("start...")


    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
