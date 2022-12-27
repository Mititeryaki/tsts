from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 27090504
    API_HASH = "47414bd130fcdf88b5546b116a779058"
    # the name to display in your alive message
    ALIVE_NAME = "mitigangbottel"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://bytclqqc:Ni3b-Op06yuxW3W7m0Nj92jJq0FBZm5v@mel.db.elephantsql.com/bytclqqc"
    # Extermnal Plugins
    EXTERNAL_REPO = False
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    LEGEND_STRING = "BACBmr2CH49CHDwLypaF5OpKqGupvOZfzfJkGYpSFPE1rj0nWxiyl99FLgTRU3URFXMPxlcfZOQqVatGOlkfCBehv59hPK4rFJ3fEcEA9Fj0z3QbJPv0ZzaLFIk9Pv3QDSRnOn0xQeRXVo4dhjI6CUCtpa6dMbIkdlLJ5tHvrjI1U6Uzgj93EPwOcPSqaOjuNS76aiuofOCaElFFCmAn29_K0lGyBou6JKXYJJECWEzRUilGpJZc8HrBG8-QdkeOa2R5qDzhnnAD2Umr-Kxkzp3Gqh9ZgcHMKdkqt1Axw2yfBHvXFs0AVLvFwFN5ERPKYQpySrg4vtTqwj0GNLGrEN2dAAAAAVDnzhAA"
    # Get in from bot father
    BOT_TOKEN = "5910828786:AAGk4kH0zYSiEFHmG2axeWf1wjGBdCk25ng"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    # PRIVATE_GROUP_BOT_API_ID = -100
    # command handler
    HANDLER = "."
    # command hanler for sudo
    SUDO_HANDLER = "5652336144"
