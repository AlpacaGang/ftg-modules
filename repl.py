from .. import loader, utils
# from telethon import*
from telethon import functions, types

import logging
import datetime
import time
import asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(REPLMod())


@loader.tds
class REPLMod(loader.Module):
    """REPLIED for selected users"""
    strings = {"name": "REPL"}

    d = dict()

    def __init__(self):
        self.name = self.strings["name"]

    def config_complete(self):
        pass

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    async def addtxcmd(self, message):
        """Select users\nFor example: .addtx used_id \"text when reply (Default: \'.\'\""""
        args = utils.get_args(message)
        if not len(args):
            await utils.answer(message, "Напиши .help REPL, там есть пример, как нужно делать.\nТы сделал неправильно!")
        elif len(args) == 1:
            self.d[int(args[0])] = '.'
        else:
            f = ""
            for i in range(1, len(args)):
                f += args[i]
                if i != len(args) - 1:
                    f += " "
            self.d[int(args[0])] = f
        await utils.answer(message, "Done.\nP.S: 3 seconds later it's automatic delete")
        await asyncio.sleep(3)
        await message.delete()

    async def clrtxcmd(self, message):
        """Unselect user\nFor example: `.clrtx used_id` for one user or `.clrtx` for all users"""
        args = utils.get_args(message)
        if not len(args):
            self.d.clear()
        else:
            self.d.pop(int(args[0]))
        await utils.answer(message, "Done.\nP.S: 3 seconds later it's automatic delete")
        await asyncio.sleep(3)
        await message.delete()

    async def watcher(self, message):
        if (message.from_id in self.d) and (
                message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id):
            await message.respond(self.d[message.from_id], reply_to=message)
