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
    """Кто читает тот гей"""
    strings = {"name": "dice"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def dicecmd(self, message):
        """Эта команда для того чтобы кинуть кубик и получить случайное значение от 1 до 6"""
        await message.delete()
        bebi = message.id()
        await message.respond(str(bebi))
#         await message.dice()
