import os
import time

from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls


__version__ = "v0.1"


# Load .env for local deployment
if os.path.exists(".env"):
    load_dotenv(".env")


# =========================
# Environment Variables
# =========================

API_ID_RAW = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

HNDLR = os.getenv("HNDLR", ".")
SUDO_USERS_RAW = os.getenv("SUDO_USERS", "")

ALIVE_PIC = os.getenv("ALIVE_PIC", "")
ALIVE_MSG = os.getenv("ALIVE_MSG", "")
PING_MSG = os.getenv("PING_MSG", "")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL")


# =========================
# Validate Required Variables
# =========================

if not API_ID_RAW:
    raise RuntimeError("API_ID is missing from environment variables.")

if not API_HASH:
    raise RuntimeError("API_HASH is missing from environment variables.")

if not SESSION:
    raise RuntimeError("SESSION is missing from environment variables.")

if not SUDO_USERS_RAW:
    raise RuntimeError("SUDO_USERS is missing from environment variables.")


try:
    API_ID = int(API_ID_RAW)
except ValueError:
    raise RuntimeError("API_ID must be a valid integer.")


try:
    SUDO_USERS = [
        int(user_id)
        for user_id in SUDO_USERS_RAW.split()
        if user_id.strip()
    ]
except ValueError:
    raise RuntimeError(
        "SUDO_USERS must contain only numeric Telegram user IDs."
    )


# =========================
# Contact Filter
# =========================

contact_filter = filters.create(
    lambda _, __, message: (
        message.from_user
        and message.from_user.is_contact
    )
    or message.outgoing
)


# =========================
# Pyrogram Client
# =========================

print("Initializing Pyrogram CLIENT...")

bot = Client(
    name="meow_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    plugins=dict(root="Modules"),
)

print("Pyrogram CLIENT initialized.")


# =========================
# PyTgCalls
# =========================

call_py = PyTgCalls(bot)


# =========================
# Other Settings
# =========================

hl = HNDLR[0] if HNDLR else "."

start_time = time.time()
