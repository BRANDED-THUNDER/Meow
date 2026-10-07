import os
import time
import base64
import binascii

from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import PyTgCalls


__version__ = "v0.1"


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

API_ID_RAW = os.getenv("API_ID", "").strip()
API_HASH = os.getenv("API_HASH", "").strip()
SESSION = os.getenv("SESSION", "").strip()

HNDLR = os.getenv("HNDLR", ".").strip()

ALIVE_PIC = os.getenv("ALIVE_PIC", "").strip()
ALIVE_MSG = os.getenv("AlIVE_MSG", "").strip()
PING_MSG = os.getenv("PING_MSG", "").strip()

LOGS_CHANNEL = os.getenv("LOGS_CHANNEL", "").strip()


# ============================================================
# API ID
# ============================================================

try:
    API_ID = int(API_ID_RAW)
except (TypeError, ValueError):
    API_ID = 0


# ============================================================
# SUDO USERS
# ============================================================

SUDO_USERS = []

sudo_raw = os.getenv("SUDO_USERS", "").strip()

if sudo_raw:
    for user_id in sudo_raw.replace(",", " ").split():
        try:
            SUDO_USERS.append(int(user_id))
        except ValueError:
            pass


# ============================================================
# VALIDATION
# ============================================================

if API_ID <= 0:
    raise ValueError(
        "API_ID is missing or invalid. "
        "Please set a valid numeric API_ID."
    )


if not API_HASH:
    raise ValueError(
        "API_HASH is missing. "
        "Please set API_HASH in Heroku Config Vars."
    )


if not SESSION:
    raise ValueError(
        "SESSION is missing. "
        "Please set SESSION in Heroku Config Vars."
    )


# ============================================================
# SESSION DIAGNOSTICS
# ============================================================
#
# IMPORTANT:
# We NEVER print the actual SESSION.
#
# This helps identify:
# - incomplete SESSION
# - corrupted SESSION
# - wrong base64 format
# - wrong decoded size
#
# ============================================================

print("========================================")
print("PYROGRAM SESSION CHECK")
print("========================================")

print(
    f"SESSION characters: {len(SESSION)}"
)

try:
    padded_session = SESSION + (
        "=" * (-len(SESSION) % 4)
    )

    decoded_session = base64.urlsafe_b64decode(
        padded_session
    )

    print(
        f"SESSION decoded bytes: {len(decoded_session)}"
    )

except (binascii.Error, ValueError, TypeError) as e:
    print(
        f"SESSION base64 decode failed: {e}"
    )

print("========================================")


# ============================================================
# CONTACT FILTER
# ============================================================

contact_filter = filters.create(
    lambda _, __, message:
        (
            message.from_user
            and message.from_user.is_contact
        )
        or message.outgoing
)


# ============================================================
# PYROGRAM CLIENT
# ============================================================
#
# Compatible with the existing Pyrogram 1.4.16 setup.
#
# IMPORTANT:
# Do NOT use:
#
#     session_string=SESSION
#
# SESSION is passed as the first positional argument.
#
# ============================================================

print("Initializing Pyrogram CLIENT...")

bot = Client(
    SESSION,
    API_ID,
    API_HASH,
    plugins=dict(root="Modules"),
)


# ============================================================
# PYTGCALLS
# ============================================================

call_py = PyTgCalls(bot)


# ============================================================
# OTHER GLOBALS
# ============================================================

hl = HNDLR[0] if HNDLR else "."

start_time = time.time()


print("Pyrogram CLIENT configuration loaded.")


### Ab deploy ke baad log mein ye aayega:

```text
========================================
PYROGRAM SESSION CHECK
========================================
SESSION characters: XXXXX
SESSION decoded bytes: XXXXX
========================================
Initializing Pyrogram CLIENT...

**Actual session string kahin print nahi hogi.**

Agar phir:

```text
unpack requires a buffer of 267 bytes
```

aata hai, to mujhe sirf ye 2 values bhejna:

```text
SESSION characters: ?
SESSION decoded bytes: ?
```

`SESSION` khud **bilkul mat bhejna**.

Ek aur important cheez: `requirements.txt` mein abhi bhi exactly:

```text
pyrogram==1.4.16
```

hona chahiye. `2.0.x` ya `2.2.26` mix mat karna.
