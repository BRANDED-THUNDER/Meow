import os
import time

from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls


__version__ = "v0.1"


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# ENV VARIABLES
# =========================

try:
    API_ID = int(os.getenv("API_ID", "0"))
except ValueError:
    API_ID = 0

API_HASH = os.getenv("API_HASH", "").strip()
SESSION = os.getenv("SESSION", "").strip()

HNDLR = os.getenv("HNDLR", ".")
ALIVE_PIC = os.getenv("ALIVE_PIC", "")
ALIVE_MSG = os.getenv("AlIVE_MSG", "")
PING_MSG = os.getenv("PING_MSG", "")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL", None)


# =========================
# SUDO USERS
# =========================

SUDO_USERS = []

sudo_raw = os.getenv("SUDO_USERS", "").strip()

if sudo_raw:
    for user_id in sudo_raw.replace(",", " ").split():
        try:
            SUDO_USERS.append(int(user_id))
        except ValueError:
            pass


# =========================
# VALIDATION
# =========================

if API_ID == 0:
    raise ValueError("API_ID is missing or invalid.")

if not API_HASH:
    raise ValueError("API_HASH is missing.")

if not SESSION:
    raise ValueError("SESSION is missing.")


# =========================
# CONTACT FILTER
# =========================

contact_filter = filters.create(
    lambda _, __, message:
        (
            message.from_user
            and message.from_user.is_contact
        )
        or message.outgoing
)


# =========================
# PYROGRAM CLIENT
# =========================
#
# IMPORTANT:
# Pyrogram 1.4.16 does NOT accept
# session_string= as a keyword.
#
# SESSION must be the first positional
# argument.
#

print("Initializing Pyrogram CLIENT...")

bot = Client(
    SESSION,
    API_ID,
    API_HASH,
    plugins=dict(root="Modules"),
)
# =========================
# PYTGCALLS
# =========================

call_py = PyTgCalls(bot)


# =========================
# OTHER GLOBALS
# =========================

hl = HNDLR[0] if HNDLR else "."

start_time = time.time()
