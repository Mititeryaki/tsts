# \\ Created by-@LegendBoy_OP -- Github.com/LEGEND-AI //
#  \\   https://github.com/LEGEND-AI/LEGENDUSERBOT   //
#   \\       Plugin for @LegendBot_XDS            //
#    ```````````````````````````````````````````

import asyncio
import glob
import os
import re

from validators.url import url

from Legendbot import legend

from ..core.managers import eod, eor
from ..helpers.utils import _legendutils

menu_category = "tools"


# ============================@ Constants @===============================
config = "./config.py"
var_checker = [
    "APP_ID",
    "PM_LOGGER_GROUP_ID",
    "PRIVATE_CHANNEL_BOT_API_ID",
    "PRIVATE_GROUP_BOT_API_ID",
    "PLUGIN_CHANNEL",
]

default = [
    "./README.md",
    "./config.py",
    "./requirements.txt",
    "./Tgbot.session",
    "./sample_config.py",
    "./stringsetup.py",
    "./exampleconfig.py",
]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]
# ========================================================================


async def switch_branch():
    with open(config, "r") as f:
        configs = f.read()
    BRANCH = "master"
    REPO = "https://github.com/LEGEND-AI/LEGENDUSERBOT"
    for match in re.finditer(
        r"(?:(UPSTREAM_REPO|UPSTREAM_REPO_BRANCH)(?:[ = \"\']+(.*[^\"\'\n])))",
        configs,
    ):
        BRANCH = match.group(2) if match.group(1) == "UPSTREAM_REPO_BRANCH" else BRANCH
        REPO = match.group(2) if match.group(1) == "UPSTREAM_REPO" else REPO
    if REPO:
        await _legendutils.runcmd(f"git clone -b {BRANCH} {REPO} TempLegend")
        file_list = os.listdir("TempLegend")
        for file in file_list:
            await _legendutils.runcmd(f"rm -rf {file}")
            await _legendutils.runcmd(f"mv ./TempLegend/{file} ./")
        await _legendutils.runcmd("pip3 install --no-cache-dir -r requirements.txt")
        await _legendutils.runcmd("rm -rf TempLegend")
    if os.path.exists("xtraplugins"):
        await _legendutils.runcmd("rm -rf xtraplugins")
    if os.path.exists("legendvc"):
        await _legendutils.runcmd("rm -rf legendvc")


@legend.legend_cmd(
    pattern="(set|get|del) var ([\s\S]*)",
    command=("var", menu_category),
    info={
        "header": "To manage config vars.",
        "flags": {
            "set": "To set new var in vps or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "usage": [
            "{tr}set var <var name> <var value>",
            "{tr}get var <var name>",
            "{tr}del var <var name>",
        ],
        "examples": [
            "{tr}get var ALIVE_NAME",
        ],
    },
)
async def variable(event):
    """
    Manage most of ConfigVars setting, set new var, get current var, or delete var...
    """
    if not os.path.exists(config):
        return await eod(event, "`There no Config file , You can't use this plugin.`")
    cmd = event.pattern_match.group(1)
    string = ""
    match = None
    with open(config, "r") as f:
        configs = f.readlines()
    if cmd == "get":
        lol = await eor(event, "`Getting information...`")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                _, val = i.split("= ")
                return await eor(lol, "**ConfigVars**:" f"\n\n`{variable}` = `{val}`")
        await eor(
            lol, "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__"
        )
    elif cmd == "set":
        variable = "".join(event.text.split(maxsplit=2)[2:])
        lol = await eor(event, "`Setting information...`")
        if not variable:
            return await lol.edit("`.set var <ConfigVars-name> <value>`")
        value = "".join(variable.split(maxsplit=1)[1:])
        variable = "".join(variable.split(maxsplit=1)[0])
        if not value:
            return await eor(lol, "`.set var <ConfigVars-name> <value>`")
        if variable not in var_checker:
            if variable == "EXTERNAL_REPO":
                if bool(value and (value.lower() != "false")) and not url(value):
                    value = "https://github.com/LEGEND-AI/PLUGINS"
                else:
                    return await eor(
                        lol,
                        f"**There no point in setting `{variable}` with `{value}`\nUse `.del var` to delete instead.**",
                    )
            value = f'"{value}"'
        await asyncio.sleep(1)
        for i in configs:
            if variable in i:
                string += f"    {variable} = {value}\n"
                match = True
            else:
                string += i
        if match:
            await eor(lol, f"`{variable}` **successfully changed to  ->  **`{value}`")
        else:
            string += f"    {variable} = {value}\n"
            await eor(
                lol, f"`{variable}`**  successfully added with value  ->  **`{value}`"
            )
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        await switch_branch()
        await event.client.reload(lol)
    if cmd == "del":
        lol = await eor(event, "`Deleting information...`")
        await asyncio.sleep(1)
        variable = event.pattern_match.group(2).split()[0]
        for i in configs:
            if variable in i:
                match = True
            else:
                string += i
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        if not match:
            return await eor(
                lol,
                "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__",
            )
        await eor(lol, f"`{variable}` **successfully deleted.**")
        await switch_branch()
        await event.client.reload(lol)


@legend.legend_cmd(
    pattern="(re|clean)load$",
    command=("reload", menu_category),
    info={
        "header": "To reload your bot in vps/ similar to restart",
        "flags": {
            "re": "restart your bot without deleting junk files",
            "clean": "delete all junk files & restart",
        },
        "usage": [
            "{tr}reload",
            "{tr}cleanload",
        ],
    },
)
async def reload(event):
    "To reload Your bot"
    cmd = event.pattern_match.group(1)
    lol = await eor(event, "`Wait 2-3 min, reloading...`")
    if cmd == "clean":
        all_files = glob.glob("./*.*")
        removing = [file for file in all_files if file not in default]
        for i in removing:
            os.remove(i)
        for i in cmds:
            await _legendutils.runcmd(i)
    await switch_branch()
    await event.client.reload(lol)
