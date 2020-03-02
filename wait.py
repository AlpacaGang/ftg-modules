# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging
import datetime
import time

logger = logging.getLogger(__name__)


def register(cb):
    cb(AFKMod())


@loader.tds
class AFKMod(loader.Module):
    """Provides a message saying that you are unavailable"""
    strings = {"name": "wait",
               "fuck": "FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUCK"}

    # async def афкcmd(self, message):
    #     """.afk [message]"""
    #     if utils.get_args_raw(message):
    #         self._db.set(__name__, "afk", utils.get_args_raw(message))
    #     else:
    #         self._db.set(__name__, "afk", True)
    #     self._db.set(__name__, "gone", time.time())
    #     self._db.set(__name__, "ratelimit", [])
    #     await self.allmodules.log("afk", data=utils.get_args_raw(message) or None)
    #     await utils.answer(message, self.strings["gone"])

    async def wait5cmd(self, message):
        """Эта команда удаляет сообхение черезе 5 секунд"""
        await utils.answer(message, "Через 5 секунд это сообщение удалится")

        for i in range(4, -1, -1):
            await time.sleep(1)
            await utils.answer(message, "Через " + str(i) + " секунд это сообщение удалится")

        await message.delete()

    async def waitcmd(self, message):
        """Эта команда удаляет сообхение черезе n секунд, \nписать нужно так: .wait n"""
        args = utils.get_args(message)
        if not args or len(args) > 1:
            await utils.answer(message, "Вы не указали число секунд или указали несколько параметров")
        else:
            try:
                x = int(args[0])
                await utils.answer(message, "Через " + str(x) + " секунд это сообщение удалится")

                for i in range(x - 1, -1, -1):
                    time.sleep(1)
                    await utils.answer(message, "Через " + str(i) + " секунд это сообщение удалится")

                await message.delete()
            except:
                await utils.answer(message, "Вы указали не число!")

    # async def chkkkcmd(self, message):
    #
    #     args = utils.get_args(message)
    #
    #     await utils.answer(message, str(args))


    # async def afkcmd(self, message):
    #     """.afk [message]"""
    #     if utils.get_args_raw(message):
    #         self._db.set(__name__, "afk", utils.get_args_raw(message))
    #     else:
    #         self._db.set(__name__, "afk", True)
    #     self._db.set(__name__, "gone", time.time())
    #     self._db.set(__name__, "ratelimit", [])
    #     await self.allmodules.log("afk", data=utils.get_args_raw(message) or None)
    #     await utils.answer(message, self.strings["gone"])
    #
    # async def fuckcmd(self, message):
    #     await utils.answer(message, self.strings["fuck"])
    #
    # async def expcmd(self, message):
    #     """ВНИМАНИЕ! ЧЕРЕЗВЫЧАЙНО ЭКСПЕРИМЕНТАЛЬНО!"""
    #     await utils.answer(message, self.strings["fuck"])
