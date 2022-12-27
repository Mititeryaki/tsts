from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 3
    API_HASH = "Your Value"
    # the name to display in your alive message
    ALIVE_NAME = "LegendBoy"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "Your Value"
    # Extermnal Plugins
    EXTERNAL_REPO = "https://github.com/LEGEND-AI/PLUGINS"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    LEGEND_STRING = "your Value"
    # Get in from bot father
    BOT_TOKEN = "Your Value"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -100
    # command handler
    HANDLER = "."
    # command hanler for sudo
    SUDO_HANDLER = "."
