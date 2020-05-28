import requests as rq
from urllib.parse import quote_plus as escape
import re

from .. import loader, utils
import asyncio
import logging
logger = logging.getLogger(__name__)

# simplified cuttly api
class CuttlyApi:
    def __init__(self, token, api_url='https://cutt.ly/api/api.php'):
        self.token = token
        self.api_url = api_url
        self.error_codes = {
            1: 'Link is already shortened',
            2: 'Link to short is not a link',
            3: 'Short link https://cutt.ly/{name} is taken',
            4: 'Invalid API key',
            5: 'Link preferred alias contains invalid characters',
            6: 'Link is from blocked domain'
        }
        self.ok_code = 7
    
    def shorten(self, short: str, name: str=None) -> dict:
        if not re.fullmatch(r'\w+://.+', short): # add scheme if needed
            short = 'http://' + short # assume that it supports http
        res = rq.get(self.api_url, params={
            "key": self.token,
            "short": escape(short, ':/%._-'),
            "name": name
        })
        res = res.json()['url']
        return res

@loader.tds
class CuttlyMod(loader.Module):
    """URL shortener module"""
    # make errors translatable
    strings = {
        "name": "Cutt.ly",
        "error_1": "<b>Link is already shortened</b>",
        "error_2": "<b>It is not a link</b>",
        "error_3": "<b>Short link https://cutt.ly/{name} is taken</b>",
        "error_4": "<b>Invalid API key. Change it in config.</b>",
        "error_5": "<b>Link preferred alias contains invalid characters</b>",
        "error_6": "<b>Link is from blocked domain</b>",
        "unknown_error": "<b>Unknown error {}. Check https://cutt.ly/cuttly-api for information.</b>",
        "ok": "<b>Shorted!</b>\nShort link: {short}\nFull link: {full}",
        "ok_nofull": "<b>Shorted!</b>\nShort link: {short}",
        "no_args": "<b>At least 1 argument needed - the link you gonna to short</b>",
        "many_args": "<b>At most 2 arguments - the link you gonna to short and preferred alias for it."
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            # name - default - description
            "cuttly_api_url", "https://cutt.ly/api/api.php", "Cuttly API URL, took from https://cutt.ly/cuttly-api",
            "api_key", None, "API key for cutt.ly. Register there and take one.",
            "include_full_link", True, "Shall bot include full link into answer."   
        )
    
    def config_complete(self):
        self.name = self.strings['name']
        self.cl = CuttlyApi(self.config['api_key'], self.config['cuttly_api_url'])
    
    async def shortcmd(self, message):
        '''usage: .short <link_to_short> [preferred_alias]'''
        args = utils.get_args(message)
        if len(args) < 1:
            await utils.answer(message, self.strings['no_args'])
            return
        elif len(args) > 2:
            await utils.answer(message, self.strings['many_args'])
            return
        
        if len(args) == 1:
            args.append(None)

        res = self.cl.shorten(*args)
        logger.debug(f'Got response from cutt.ly: {res}')
        if res['status'] != self.cl.ok_code:
            try:
                msg = self.strings[f'error_{res["status"]}']
            except KeyError: # Unknown error, not in strings yet
                msg = self.strings['unknown_error'].format(res['status'])
        else:
            if self.config['include_full_link']:
                msg = self.strings['ok']
            else:
                msg = self.strings['ok_nofull']
        await utils.answer(message, msg.format(
            short = res.get('shortLink', None), # If we got an error
            full = res.get('fullLink', None),
            name = args[1]
        ))
