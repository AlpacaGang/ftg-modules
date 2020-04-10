from .. import loader, utils

import logging
import datetime
import time
import asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(WAITMod())


@loader.tds
class WAITMod(loader.Module):
    """Кто читает тот гей"""
    strings = {"name": "wait"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def dicecmd(self, message):
        """Эта команда для того чтобы кинуть кубик и получить случайное значение от 1 до 6"""
        await message.delete()
        await utils.answer(message, "🎲")
