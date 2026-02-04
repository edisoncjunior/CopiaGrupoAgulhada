Funcionou em 04/02 as 00h42
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

try:
    from dotenv import load_dotenv
    if os.path.exists(".env"):
        load_dotenv()
        print("[ENV] .env carregado (execução local)")
    else:
        print("[ENV] .env não encontrado (execução web)")
except ImportError:
    print("[ENV] python-dotenv não instalado (execução web)")

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SOURCE_CHAT_ID = int(os.environ["SOURCE_CHAT_ID"])
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])
SESSION_STRING = os.environ.get("TELEGRAM_SESSION_STRING")

if not SESSION_STRING:
    raise RuntimeError("TELEGRAM_SESSION_STRING não definida")

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_message(event):
    try:
        if event.message.media:
            await client.send_file(
                TARGET_CHAT_ID,
                event.message.media,
                caption=event.message.text
            )
        else:
            await client.send_message(
                TARGET_CHAT_ID,
                event.message.text
            )
        print("Mensagem encaminhada com sucesso")
    except Exception as e:
        print(f"Erro ao encaminhar mensagem: {e}")

async def main():
    print("Bot de encaminhamento iniciado...")
    await client.connect()

    if not await client.is_user_authorized():
        raise RuntimeError("Sessão Telegram inválida ou expirada")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
