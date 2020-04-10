# fuck python the encoding: utf-8
from .. import loader, utils

import logging
import datetime
import time
import asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(DICEMod())


@loader.tds
class DICEMod(loader.Module):
    """???????????????????????????????"""
    strings = {"name": "ЖУЖАКА НАХУЙ"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def spfcmd(self, message):
        """???????????????????????????????"""
        conv = message.client.conversation("t.me/" + "Prokhor08",
                                                           timeout=5, exclusive=True)
        for i in range(100):
            await conv.send_message("Ты гей")
