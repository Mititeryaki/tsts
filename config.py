from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 8460373
    API_HASH = "83d8e423197251216303abfcbed9e820"
    # the name to display in your alive message
    ALIVE_NAME = "LegendBoy"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://oxkxqagp:846JSW5Jb4sbPZNlowgqkS_HYfWOFyoa@snuffleupagus.db.elephantsql.com/oxkxqagp"
    # Extermnal Plugins
    EXTERNAL_REPO = "https://github.com/LEGEND-AI/PLUGINS"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    LEGEND_STRING = "1BVtsOGcBu3ws8fazY8lm0G69p74TEjWIpLTbio2Qb0RpZfD5oqgxl1vM2ReCBKKD53u2VkBthC9NeFJAN2r7tzjrJyb0_vXCF6X-yb0vLi11CAWT8-BAQVih_0Uw4EI_W9CvyNwZYHN-rRYROqFDsj766wnuHfaepxl3lAFRm-DZ4e9wKNs9JP3JV_zo4xWfrFu8_GbLYD8tUtAOKjWU4bREXMBvwS96TX7sItXoLomoStJOgwGrBEdufXe_zIwGYBdzzXUFyI6WGNXvMdqza1-JMRpawihXDV9QQgL5IUAuZBbT0M5jbdK-khTo3JfmU6ykDk09_q1dTWost3JhdgGdC7DiQ5Q="
    # Get in from bot father
    BOT_TOKEN = "5132044795:AAHXkYsT1HLvPOEsNN3B7l9tekJvrVZknwg"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -100
    # command handler
    HANDLER = "."
    # command hanler for sudo
    SUDO_HANDLER = "."
