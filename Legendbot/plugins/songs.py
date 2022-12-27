# by  @krishna1709 ( https://t.me/mrconfused  )

# songs finder for legenduserbot
import base64
import contextlib
import io
import os

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import eod, eor
from ..helpers.functions import delete_conv, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import reply_id
from . import legend, song_download

menu_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@legend.legend_cmd(
    pattern="song(320)?(?:\s|$)([\s\S]*)",
    command=("song", menu_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def song(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await eor(event, "`What I am Supposed to find `")
    lol = base64.b64decode("MFdZS2llTVloTjAzWVdNeA==")
    legendevent = await eor(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await legendevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_file, legendthumb, title = await song_download(
        video_link, legendevent, quality=q
    )
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"**Title:** `{title}`",
        thumb=legendthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await legendevent.delete()
    for files in (legendthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


@legend.legend_cmd(
    pattern="vsong(?:\s|$)([\s\S]*)",
    command=("vsong", menu_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def vsong(event):
    "To search video songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await eor(event, "`What I am Supposed to find`")
    lol = base64.b64decode("MFdZS2llTVloTjAzWVdNeA==")
    legendevent = await eor(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await legendevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    with contextlib.suppress(BaseException):
        lol = Get(lol)
        await event.client(lol)
    vsong_file, legendthumb, title = await song_download(
        video_link, legendevent, video=True
    )
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        caption=f"**Title:** `{title}`",
        thumb=legendthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await legendevent.delete()
    for files in (legendthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@legend.legend_cmd(
    pattern="(s(ha)?z(a)?m)(?:\s|$)([\s\S]*)",
    command=("shazam", menu_category),
    info={
        "header": "To reverse search song.",
        "description": "Reverse search audio file using shazam api",
        "flags": {"s": "To send the song of sazam match"},
        "usage": [
            "{tr}shazam <reply to voice/audio>",
            "{tr}szm <reply to voice/audio>",
            "{tr}szm s<reply to voice/audio>",
        ],
    },
)
async def shazamcmd(event):
    "To reverse search song."
    reply = await event.get_reply_message()
    mediatype = await media_type(reply)
    chat = "@DeezerMusicBot"
    delete = False
    flag = event.pattern_match.group(4)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await eod(
            event, "__Reply to Voice clip or Audio clip to reverse search that song.__"
        )
    legendevent = await eor(event, "__Downloading the audio clip...__")
    name = "lol.mp3"
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await eod(
            legendevent, f"**Error while reverse searching song:**\n__{e}__"
        )

    file = track["images"]["background"]
    title = track["share"]["subject"]
    slink = await yt_search(title)
    if flag == "s":
        deezer = track["hub"]["providers"][1]["actions"][0]["uri"][15:]
        async with event.client.conversation(chat) as conv:
            try:
                purgeflag = await conv.send_message("/start")
            except YouBlockedUserError:
                await legend(unblock("DeezerMusicBot"))
                purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(deezer)
            await event.client.get_messages(chat)
            song = await event.client.get_messages(chat)
            await song[0].click(0)
            await conv.get_response()
            file = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            delete = True
    await event.client.send_file(
        event.chat_id,
        file,
        caption=f"<b>Song :</b> <code>{title}</code>\n<b>Song Link : <a href = {slink}/1>YouTube</a></b>",
        reply_to=reply,
        parse_mode="html",
    )
    await legendevent.delete()
    if delete:
        await delete_conv(event, chat, purgeflag)


@legend.legend_cmd(
    pattern="song2(?:\s|$)([\s\S]*)",
    command=("song2", menu_category),
    info={
        "header": "To search songs and upload to telegram",
        "description": "Searches the song you entered in query and sends it quality of it is 320k",
        "usage": "{tr}song2 <song name>",
        "examples": "{tr}song2 memories",
    },
)
async def song2(event):
    "To search songs"
    song = event.pattern_match.group(1)
    chat = "@LegendMusicRobot"
    reply_id_ = await reply_id(event)
    legendevent = await eor(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message(song)
        except YouBlockedUserError:
            await legend(unblock("LegendMusicRobot"))
            purgeflag = await conv.send_message(song)
        music = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if not music.media:
            return await eod(legendevent, SONG_NOT_FOUND, parse_mode="html")
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>Title :- <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await legendevent.delete()
        await delete_conv(event, chat, purgeflag)
