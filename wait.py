from .. import loader, utils

import logging
import datetime
import time

logger = logging.getLogger(__name__)


def register(cb):
    cb(WAITMod())


@loader.tds
class WAITMod(loader.Module):
    """Provides a message saying that you are unavailable"""
    strings = {"name": "wait",
               "fuck": "FUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUCK"}
    
    def config_complete(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

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
    
    async def tagcmd(self, message):
        """Эта команда для троллинга друзей. \nЕй вы можете тегнуть друга, а сообщение само удалится!"""
        await message.delete()
