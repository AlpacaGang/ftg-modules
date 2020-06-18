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
    """Этот модуль поможет вам удалить сообщение через n секунд/минут"""
    strings = {"name": "wait"}

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def wait5cmd(self, message):
        """Эта команда удаляет сообхение черезе 5 секунд"""
        await utils.answer(message, "Через 5 секунд это сообщение удалится")

        for i in range(4, -1, -1):
            await asyncio.sleep(1)
            await utils.answer(message, "Через " + str(i) + " секунд это сообщение удалится")

        await message.delete()

    async def waitcmd(self, message):
        """Эта команда удаляет сообхение через n секунд, \nписать нужно так: .wait <n>, если хотите секунды\nи так .wait <n>m, если хотите ждать в минутах\n(например .wait 5m)"""
        args = utils.get_args(message)
        if not args or len(args) > 1:
            await utils.answer(message, "Вы не указали число секунд или указали несколько параметров")
        else:
            try:
                g = -1
                h = ""
                try:
                    g = int(args[0][:len(args[0])])
                except:
                    try:
                        g = int(args[0][:len(args[0]) - 1])
                        h = args[0][len(args[0]) - 1]
                    except:
                        await utils.answer(message, "Вы указали не число!")
                if g > 0:
                    if h == 's' or h == '':
                        x = g
                        lst = "Через " + str(x) + " секунд это сообщение удалится"
                        await utils.answer(message, lst)

                        dd = time.time()

                        while time.time() - dd < x:
                            now = "Через " + str(x - round(time.time() - dd)) + " секунд это сообщение удалится"
                            if now != lst:
                                await utils.answer(message, now)
                            lst = now
                        await message.delete()
                    elif h == 'm':
                        x = g
                        lst = "Через " + str(x) + " минут это сообщение удалится"
                        await utils.answer(message, lst)

                        dd = time.time()

                        ff = x * 60

                        llst = x
                        while time.time() - dd < ff:
                            oo = round((ff - round(time.time() - dd)) / 60)
                            nw = oo
                            if nw == llst:
                                await asyncio.sleep(0.1)
                                continue
                            now = "Через " + str(nw) + " минут это сообщение удалится"
                            await utils.answer(message, now)
                            llst = nw
                        await message.delete()
                    else:
                        await utils.answer(message, "Вы указали не число!")
            except:
                await utils.answer(message, "Упс, ошибочка вышла! Напшите @gerasikoff, он вам поможет")

    async def tagcmd(self, message):
        """Эта команда для троллинга друзей. \nЕй вы можете тегнуть друга, а сообщение само удалится!"""
        await message.delete()
