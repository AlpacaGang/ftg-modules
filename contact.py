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

    async def contactmd(self, message):
        """Эта команда пишет 10 сообщений для контакта"""
        try:
            await message.delete()
            x = 10
            lst = str(x)
            await utils.respond(message, lst)

            dd = time.time()

            while time.time() - dd < x:
                now = str(x - round(time.time() - dd))
                if now != lst:
                    await utils.respond(message, now)
                lst = now
        except:
            await utils.answer(message, "Упс, ошибочка вышла! Напшите @gerasikoff, он вам поможет")
