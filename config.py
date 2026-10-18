from os import getenv
from dotenv import load_dotenv

load_dotenv()
AID_Token = getenv("Bot_token")
CHAT_ID = getenv("Chat_id")

def load_env(request):
    if request == "token":
        return AID_Token
    elif request == "id":
        return CHAT_ID
