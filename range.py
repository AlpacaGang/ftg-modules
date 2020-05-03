# encoding: utf-8
from .. import loader, utils

import asyncio
import logging
logger = logging.getLogger(__name__)


def register(cb):
    cb(RangeMod())


@loader.tds
class RangeMod(loader.Module):
    """Provides numbers as in Python range with delay"""
    strings = {
        "name": "Range", 
        "no_args": "<b>Usage: .range &lt;delay&gt; &lt;py_range_args&gt; </b>",
        "delay_num": "<b>Delay must be a number</b>",
        "args_int": "<b>All range args must be integers</b>",
        "many_args": "<b>There should be no more than 4 arguments</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "msg_format", "{0}", "Format of each message. {0} replaces current number."
        )
        self.name = self.strings['name']
    
    def config_complete(self):
        self.name = self.strings['name']

    async def rangecmd(self, message):
        """Iterates over the given range and returns each number in separate message.\nUsage: .range <delay> <python_range_args>"""
        args = utils.get_args(message)
        if len(args) < 2:
            logger.warning(f'Minimum 2 args; {len(args)} provided')
            await utils.answer(message, self.strings['no_args'])
            return
        elif len(args) > 4:
            logger.warning(f'Maximum 4 args; {len(args)} provided')
            await utils.answer(message, self.strings['many_args'])
            return

        try:
            delay = float(args[0])
        except ValueError:
            logger.warning(f'Impossible to convert delay to float ({args[0]})')
            await utils.answer(message, self.strings['delay_num'])
            return
        
        try:
            range_args = args[1:]
            range_args = [int(x) for x in range_args]
        except ValueError:
            logger.warning(f'Impossible to convert all range args to int ({range_args})')
            await utils.answer(message, self.strings['args_int'])
            return
        
        logger.debug(f'Range arguments are {range_args}, delay is {delay}')
        await message.delete()
        for now in range(*range_args):
            await message.respond(self.config['msg_format'].format(now))
            await asyncio.sleep(delay)


        
