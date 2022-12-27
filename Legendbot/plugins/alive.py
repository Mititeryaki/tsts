import random
import re
import time
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from Legendbot import StartTime, legend, legendversion

from ..Config import Config
from ..core.managers import eor
from ..helpers.functions import check_data_base_heal_th, get_readable_time, legendalive
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

menu_category = "utils"


@legend.legend_cmd(
    pattern="alive$",
    command=("alive", menu_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    ANIME = None
    legend_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    if "ANIME" in legend_caption:
        data = requests.get("https://animechan.vercel.app/api/random").json()
        ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    legendevent = await eor(event, "`Checking...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**✮ MY BOT IS RUNNING SUCCESSFULLY ✮**"
    CAT_IMG = gvarstatus("ALIVE_PIC")
    caption = legend_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        ANIME=ANIME,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        legendver=legendversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if CAT_IMG:
        CAT = list(CAT_IMG.split())
        PIC = random.choice(CAT)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await legendevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await eor(
                legendevent,
                f"**Media Value Error!!**\n__Change the link by __`.setdb`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await eor(
            legendevent,
            caption,
        )


temp = """{ALIVE_TEXT}
**{EMOJI} Database :** `{dbhealth}`
**{EMOJI} Telethon Version :** `{telever}`
**{EMOJI} Legenduserbot Version :** `{legendver}`
**{EMOJI} Python Version :** `{pyver}`
**{EMOJI} Uptime :** `{uptime}`
**{EMOJI} Master:** {mention}"""


def legendalive_text():
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    legend_caption = "**Legenduserbot is Up and Running**\n"
    legend_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    legend_caption += f"**{EMOJI} Legenduserbot Version :** `{legendversion}`\n"
    legend_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    legend_caption += f"**{EMOJI} Master:** {mention}\n"
    return legend_caption


@legend.legend_cmd(
    pattern="ialive$",
    command=("ialive", menu_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}ialive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    results = await event.client.inline_query(Config.BOT_USERNAME, "ialive")
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@legend.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await legendalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
