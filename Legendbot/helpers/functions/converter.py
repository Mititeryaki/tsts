import os

from PIL import Image

from Legendbot.core.logger import logging
from Legendbot.core.managers import eor
from Legendbot.helpers.functions.vidtools import take_screen_shot
from Legendbot.helpers.tools import fileinfo, media_type, meme_type
from Legendbot.helpers.utils.utils import runcmd

LOGS = logging.getLogger(__name__)


class LegendConverter:
    async def _media_check(self, reply, dirct, file, memetype):
        if not os.path.isdir(dirct):
            os.mkdir(dirct)
        legendfile = os.path.join(dirct, file)
        if os.path.exists(legendfile):
            os.remove(legendfile)
        try:
            legendmedia = reply if os.path.exists(reply) else None
        except TypeError:
            if memetype in ["Video", "Gif"]:
                dirct = "./temp/legendfile.mp4"
            elif memetype == "Audio":
                dirct = "./temp/legendfile.mp3"
            legendmedia = await reply.download_media(dirct)
        return legendfile, legendmedia

    async def to_image(
        self, event, reply, dirct="./temp", file="meme.png", noedits=False, rgb=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype == "Document":
            return event, None
        legendevent = (
            event
            if noedits
            else await eor(event, "`Transfiguration Time! Converting to ....`")
        )
        legendfile, legendmedia = await self._media_check(reply, dirct, file, memetype)
        if memetype == "Photo":
            im = Image.open(legendmedia)
            im.save(legendfile)
        elif memetype in ["Audio", "Voice"]:
            await runcmd(f"ffmpeg -i '{legendmedia}' -an -c:v copy '{legendfile}' -y")
        elif memetype in ["Round Video", "Video", "Gif"]:
            await take_screen_shot(legendmedia, "00.00", legendfile)
        if mediatype == "Sticker":
            if memetype == "Animated Sticker":
                legendcmd = f"lottie_convert.py --frame 0 -if lottie -of png '{legendmedia}' '{legendfile}'"
                stdout, stderr = (await runcmd(legendcmd))[:2]
                if stderr:
                    LOGS.info(stdout + stderr)
            elif memetype == "Video Sticker":
                await take_screen_shot(legendmedia, "00.00", legendfile)
            elif memetype == "Static Sticker":
                im = Image.open(legendmedia)
                im.save(legendfile)
        if legendmedia and os.path.exists(legendmedia):
            os.remove(legendmedia)
        if os.path.exists(legendfile):
            if rgb:
                img = Image.open(legendfile)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(legendfile)
            return legendevent, legendfile, mediatype
        return legendevent, None

    async def to_sticker(
        self, event, reply, dirct="./temp", file="meme.webp", noedits=False, rgb=False
    ):
        filename = os.path.join(dirct, file)
        response = await self.to_image(event, reply, noedits=noedits, rgb=rgb)
        if response[1]:
            image = Image.open(response[1])
            image.save(filename, "webp")
            os.remove(response[1])
            return response[0], filename, response[2]
        return response[0], None

    async def to_webm(
        self, event, reply, dirct="./temp", file="animate.webm", noedits=False
    ):
        # //Hope u dunt kang :/ @LegendBoy_OP
        memetype = await meme_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Gif",
            "Video",
        ]:
            return event, None
        legendevent = (
            event
            if noedits
            else await eor(event, "__🎞Converting into Animated sticker..__")
        )
        legendfile, legendmedia = await self._media_check(reply, dirct, file, memetype)
        media = await fileinfo(legendmedia)
        h = media["height"]
        w = media["width"]
        w, h = (-1, 512) if h > w else (512, -1)
        await runcmd(
            f"ffmpeg -to 00:00:02.900 -i '{legendmedia}' -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an '{legendfile}'"
        )  # pain
        if os.path.exists(legendmedia):
            os.remove(legendmedia)
        if os.path.exists(legendfile):
            return legendevent, legendfile
        return legendevent, None

    async def to_gif(
        self, event, reply, dirct="./temp", file="meme.mp4", maxsize="5M", noedits=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Animated Sticker",
            "Video",
            "Gif",
        ]:
            return event, None
        legendevent = (
            event
            if noedits
            else await eor(event, "`Transfiguration Time! Converting to ....`")
        )
        legendfile, legendmedia = await self._media_check(reply, dirct, file, memetype)
        if mediatype == "Sticker":
            if memetype == "Video Sticker":
                await runcmd(f"ffmpeg -i '{legendmedia}' -c copy '{legendfile}'")
            elif memetype == "Animated Sticker":
                await runcmd(f"lottie_convert.py '{legendmedia}' '{legendfile}'")
        if legendmedia.endswith(".gif"):
            await runcmd(
                f"ffmpeg -f gif -i '{legendmedia}' -fs {maxsize} -an '{legendfile}'"
            )
        else:
            await runcmd(
                f"ffmpeg -i '{legendmedia}' -c:v libx264 -fs {maxsize} -an '{legendfile}'"
            )
        if legendmedia and os.path.exists(legendmedia):
            os.remove(legendmedia)
        if os.path.exists(legendfile):
            return legendevent, legendfile
        return legendevent, None


Convert = LegendConverter()
