# collage plugin for legenduserbot by @krishna1709

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.import os

import os

from Legendbot import Convert, legend

from ..core.managers import eod, eor
from ..helpers import _legendutils, meme_type, reply_id

menu_category = "utils"


@legend.legend_cmd(
    pattern="collage(?:\s|$)([\s\S]*)",
    command=("collage", menu_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    legendinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    lolid = await reply_id(event)
    if not (reply and (reply.media)):
        return await eod(event, "`Reply to a media file..`")
    mediacheck = await meme_type(reply)
    if mediacheck not in [
        "Round Video",
        "Gif",
        "Video Sticker",
        "Animated Sticker",
        "Video",
    ]:
        return await eod(event, "`The replied message media type is not supported.`")
    if legendinput:
        if not legendinput.isdigit():
            return await eod(event, "`You input is invalid, check help`")

        legendinput = int(legendinput)
        if not 0 < legendinput < 10:
            await eor(
                event,
                "__Why big grid you cant see images, use size of grid between 1 to 9\nAnyways changing value to max 9__",
            )
            legendinput = 9
    else:
        legendinput = 3
    await eor(event, "```Collaging this may take several minutes..... 😁```")
    if mediacheck in ["Round Video", "Gif", "Video Sticker", "Video"]:
        if not os.path.isdir("./temp/"):
            os.mkdir("./temp/")
        legendsticker = await reply.download_media(file="./temp/")
        collagefile = legendsticker
    else:
        collage_file = await Convert.to_gif(
            event, reply, file="collage.mp4", noedits=True
        )
        collagefile = collage_file[1]
    if not collagefile:
        await eor(event, "**Error:-** __Unable to process the replied media__")
    endfile = "./temp/collage.png"
    legendcmd = f"vcsi -g {legendinput}x{legendinput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _legendutils.runcmd(legendcmd))[:2]
    if not os.path.exists(endfile) and os.path.exists(collagefile):
        os.remove(collagefile)
        return await eod(
            event, "`Media is not supported, or try with smaller grid size`"
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=lolid,
    )
    await event.delete()
    for files in (collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
