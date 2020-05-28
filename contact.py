from .. import loader, utils

import logging
import datetime
import time
import asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(CONTACTMod())


@loader.tds
class CONTACTMod(loader.Module):
    """Это модуль для игры в \"контакт\""""
    strings = {"name": "contact"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def contactcmd(self, message):
        """Эта команда пишет 10 сообщений для контакта"""
        try:
            await message.delete()
            x = 10
            lst = str(x)
            await message.respond(lst)

            dd = time.time()

            while time.time() - dd < x:
                now = str(x - round(time.time() - dd))
                if now != lst:
                    await message.respond(now)
                lst = now
        except:
            await message.respond("Упс, ошибочка вышла! Напшите @gerasikoff, он вам поможет")
