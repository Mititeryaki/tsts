import contextlib
import importlib
import sys
from pathlib import Path

from Legendbot import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import eod, eor
from ..core.session import legend
from ..helpers.utils import _format, _legendutils, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("LegendUserbot")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"Legendbot/plugins/{shortname}.py")
        checkplugins(path)
        name = f"Legendbot.plugins.{shortname}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info(f"Successfully imported {shortname}")
    else:
        if plugin_path is None:
            path = Path(f"Legendbot/plugins/{shortname}.py")
            name = f"Legendbot.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        checkplugins(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = legend
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = legend.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._legendutils = _legendutils
        mod.eod = eod
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.eor = eor
        mod.logger = logging.getLogger(shortname)
        mod.borg = legend
        spec.loader.exec_module(mod)
        # for imports
        sys.modules[f"Legendbot.plugins.{shortname}"] = mod
        LOGS.info(f"Successfully imported {shortname}")


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    legend.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    with contextlib.suppress(BaseException):
        for i in LOAD_PLUG[shortname]:
            legend.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    try:
        name = f"Legendbot.plugins.{shortname}"
        for i in reversed(range(len(legend._event_builders))):
            ev, cb = legend._event_builders[i]
            if cb.__module__ == name:
                del legend._event_builders[i]
    except BaseException as exc:
        raise ValueError from exc


def checkplugins(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)
