# credits to @mrconfused and @krishna1709
#    Copyright (C) 2020  krishna.n(π.$)

import os

from telegraph import exceptions, upload_file

from Legendbot import Convert, legend

from ..core.managers import eod, eor
from ..helpers import reply_id
from . import deEmojify, phcomment, threats, trap, trash

menu_category = "fun"


@legend.legend_cmd(
    pattern="trash$",
    command=("trash", menu_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}trash",
    },
)
async def _(event):
    "image meme creator."
    replied = await event.get_reply_message()
    lolid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="trash.png", rgb=True
    )
    if output[1] is None:
        return await eod(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    lol = f"https://graph.org{response[0]}"
    lol = await trash(lol)
    os.remove(output[1])
    await output[0].delete()
    await event.client.send_file(event.chat_id, lol, reply_to=lolid)


@legend.legend_cmd(
    pattern="threats$",
    command=("threats", menu_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}threats",
    },
)
async def _(event):
    "image meme creator."
    replied = await event.get_reply_message()
    lolid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="threats.png", rgb=True
    )
    if output[1] is None:
        return await eod(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    lol = f"https://graph.org{response[0]}"
    lol = await threats(lol)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, lol, reply_to=lolid)


@legend.legend_cmd(
    pattern="trap(?:\s|$)([\s\S]*)",
    command=("trap", menu_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "Description": "creates a trap card",
        "usage": "{tr}trap (name of the person to trap) ; (trapper name)",
    },
)
async def _(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        return await eor(
            event,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
    replied = await event.get_reply_message()
    lolid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="trap.png", rgb=True
    )
    if output[1] is None:
        return await eod(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    lol = f"https://graph.org{response[0]}"
    lol = await trap(text1, text2, lol)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, lol, reply_to=lolid)


@legend.legend_cmd(
    pattern="phub(?:\s|$)([\s\S]*)",
    command=("phub", menu_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "description": "pornhub comment creator",
        "usage": "{tr}phub (username);(text in comment)",
    },
)
async def _(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        return await eor(
            event,
            "**Syntax :** reply to image or sticker with `.phub (username);(text in comment)`",
        )
    replied = await event.get_reply_message()
    lolid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await Convert.to_image(
        event, replied, dirct="./temp", file="phub.png", rgb=True
    )
    if output[1] is None:
        return await eod(
            output[0], "__Unable to extract image from the replied message.__"
        )
    size = os.stat(output[1]).st_size
    if size > 5242880:
        os.remove(output[1])
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )

    await output[0].edit("generating image..")
    try:
        response = upload_file(output[1])
    except exceptions.TelegraphException as exc:
        os.remove(output[1])
        return await output[0].edit(f"**Error: **\n`{exc}`")
    lol = f"https://graph.org{response[0]}"
    lol = await phcomment(lol, text, username)
    await output[0].delete()
    os.remove(output[1])
    await event.client.send_file(event.chat_id, lol, reply_to=lolid)
