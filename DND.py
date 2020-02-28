# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    By Magical Unicorn (based on official Anti PM & AFK Friendly Telegram modules)
#    Copyright (C) 2020 Magical Unicorn

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

from telethon import functions, types
logger = logging.getLogger(__name__)


def register(cb):
    cb(DoNotDisturb())


@loader.tds
class DoNotDisturb(loader.Module):
    """
    DND (Do Not Disturb) :
    -> Prevents people sending you unsolicited private messages.
    -> Prevents disturbing when you are unavailable.\n
    Commands :
     
    """
    strings = {"name": "DND",
               "afk": "<b>I'm AFK right now (since</b> <i>{}</i> <b>ago).</b>",
               "afk_back": "<b>I'm goin' BACK !</b>",
               "afk_gone": "<b>I'm goin' AFK !</b>",
               "afk_no_group_off": "<b>AFK status message enabled for group chats.</b>",
               "afk_no_group_on": "<b>AFK status message disabled for group chats.</b>",
               "afk_no_pm_off": "<b>AFK status message enabled for PMs.</b>",
               "afk_no_pm_on": "<b>AFK status message disabled for PMs.</b>",
               "afk_notif_off": "<b>Notifications are now disabled during AFK time.</b>",
               "afk_notif_on": "<b>Notifications are now enabled during AFK time.</b>",
               "afk_rate_limit_off": "<b>AFK status message rate limit disabled.</b>",
               "afk_rate_limit_on": ("<b>AFK status message rate limit enabled.</b>"
                                     "\n\n<b>One AFK status message max will be sent per chat.</b>"),
               "afk_reason": ("<b>I'm AFK right now (since {} ago).</b>"
                              "\n\n<b>Reason :</b> <i>{}</i>"),
               "arg_on_off": "<b>Argument must be 'off' or 'on' !</b>",
               "pm_off": ("<b>Automatic answer for denied PMs disabled."
                          "\n\nUsers are now free to PM !</b>"),
               "pm_on": "<b>An automatic answer is now sent for denied PMs.</b>",
               "pm_allowed": "<b>I have allowed</b> <a href='tg://user?id={}'>you</a> <b>to PM now.</b>",
               "pm_blocked": ("<b>I don't want any PM from</b> <a href='tg://user?id={}'>you</a>, "
                              "<b>so you have been blocked !</b>"),
               "pm_denied": "<b>I have denied</b> <a href='tg://user?id={}'>you</a> <b>to PM now.</b>",
               "pm_go_away": ("Hey there! Unfortunately, I don't accept private messages from strangers."
                              "\n\nPlease contact me in a group, or <b>wait</b> for me to approve you."),
               "pm_reported": "<b>You just got reported to spam !</b>",
               "pm_limit_arg": "<b>Argument must be 'off', 'on' or a number between 10 and 1000 !</b>",
               "pm_limit_off": "<b>Not allowed users are now free to PM without be automatically blocked.</b>",
               "pm_limit_on": "<b>Not allowed users are now blocked after {} PMs.</b>",
               "pm_limit_current": "<b>Current limit is {}.</b>",
               "pm_limit_current_no": "<b>Automatic user blocking is currently disabled.</b>",
               "pm_limit_reset": "<b>Limit reseted to {}.</b>",
               "pm_limit_set": "<b>Limit set to {}.</b>",
               "pm_notif_off": "<b>Notifications from denied PMs are now disabled.</b>",
               "pm_notif_on": "<b>Notifications from denied PMs are now enabled.</b>",
               "pm_triggered": ("Hey! I don't appreciate you barging into my PM like this !"
                                "\nDid you even ask me for approving you to PM ? No ?"
                                "\nGoodbye then."
                                "\n\nPS: You've been reported as spam."),
               "pm_unblocked": ("<b>Alright fine! I'll forgive them this time. PM has been unblocked for</b> "
                                "<a href='tg://user?id={}'>this user</a>."),
               "unknow": ("An unknow problem as occured."
                          "\n\nPlease report problem with logs on "
                          "<a href='https://github.com/LegendaryUnicorn/FTG-Unofficial-Modules'>Github</a>."),
               "who_to_allow": "<b>Who shall I allow to PM ?</b>",
               "who_to_block": "<b>Specify who to block.</b>",
               "who_to_deny": "<b>Who shall I deny to PM ?</b>",
               "who_to_report": "<b>Who shall I report ?</b>",
               "who_to_unblock": "<b>Specify who to unblock.</b>"}

    def __init__(self):
        self._me = None
        self.default_pm_limit = 50

    def config_complete(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me(True)

    async def afkbackcmd(self, message):
        """Remove the AFK status.\n """
        self._db.set(__name__, "afk", False)
        self._db.set(__name__, "afk_gone", None)
        self._db.set(__name__, "afk_rate", [])
        await utils.answer(message, self.strings["afk_back"])

    async def afkgocmd(self, message):
        """
        .afkgo : Enable AFK status.
        .afkgo [message] : Enable AFK status and add a reason.
         
        """
        if utils.get_args_raw(message):
            self._db.set(__name__, "afk", utils.get_args_raw(message))
        else:
            self._db.set(__name__, "afk", True)
        self._db.set(__name__, "afk_gone", time.time())
        self._db.set(__name__, "afk_rate", [])
        await utils.answer(message, self.strings["afk_gone"])

    async def afknogroupcmd(self, message):
        """
        .afknogroup : Disable/Enable AFK status message for group chats.
        .afknogroup off : Enable AFK status message for group chats.
        .afknogroup on : Disable AFK status message for group chats.
         
        """
        if utils.get_args_raw(message):
            afknogroup_arg = utils.get_args_raw(message)
            if afknogroup_arg == "off":
                self._db.set(__name__, "afk_no_group", False)
                await utils.answer(message, self.strings["afk_no_group_off"])
            elif afknogroup_arg == "on":
                self._db.set(__name__, "afk_no_group", True)
                await utils.answer(message, self.strings["afk_no_group_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            afknogroup_current = self._db.get(__name__, "afk_no_group")
            if afknogroup_current is None or afknogroup_current is False:
                self._db.set(__name__, "afk_no_group", True)
                await utils.answer(message, self.strings["afk_no_group_on"])
            elif afknogroup_current is True:
                self._db.set(__name__, "afk_no_group", False)
                await utils.answer(message, self.strings["afk_no_group_off"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def afknopmcmd(self, message):
        """
        .afknopm : Disable/Enable AFK status message for PMs.
        .afknopm off : Enable AFK status message for PMs.
        .afknopm on : Disable AFK status message for PMs.
         
        """
        if utils.get_args_raw(message):
            afknopm_arg = utils.get_args_raw(message)
            if afknopm_arg == "off":
                self._db.set(__name__, "afk_no_pm", False)
                await utils.answer(message, self.strings["afk_no_pm_off"])
            elif afknopm_arg == "on":
                self._db.set(__name__, "afk_no_pm", True)
                await utils.answer(message, self.strings["afk_no_pm_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            afknopm_current = self._db.get(__name__, "afk_no_pm")
            if afknopm_current is None or afknopm_current is False:
                self._db.set(__name__, "afk_no_pm", True)
                await utils.answer(message, self.strings["afk_no_pm_on"])
            elif afknopm_current is True:
                self._db.set(__name__, "afk_no_pm", False)
                await utils.answer(message, self.strings["afk_no_pm_off"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def afknotifcmd(self, message):
        """
        .afknotif : Disable/Enable the notifications during AFK time.
        .afknotif off : Disable the notifications during AFK time.
        .afknotif on : Enable the notifications during AFK time.
         
        """
        if utils.get_args_raw(message):
            afknotif_arg = utils.get_args_raw(message)
            if afknotif_arg == "off":
                self._db.set(__name__, "afk_notif", False)
                await utils.answer(message, self.strings["afk_notif_off"])
            elif afknotif_arg == "on":
                self._db.set(__name__, "afk_notif", True)
                await utils.answer(message, self.strings["afk_notif_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            afknotif_current = self._db.get(__name__, "afk_notif")
            if afknotif_current is None or afknotif_current is False:
                self._db.set(__name__, "afk_notif", True)
                await utils.answer(message, self.strings["afk_notif_on"])
            elif afknotif_current is True:
                self._db.set(__name__, "afk_notif", False)
                await utils.answer(message, self.strings["afk_notif_off"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def afkratecmd(self, message):
        """
        .afkrate : Disable/Enable AFK rate limit.
        .afkrate off : Disable AFK rate limit.
        .afkrate on : Enable AFK rate limit. One AFK status message max will be sent per chat.
         
        """
        if utils.get_args_raw(message):
            afkrate_arg = utils.get_args_raw(message)
            if afkrate_arg == "off":
                self._db.set(__name__, "afk_rate_limit", False)
                await utils.answer(message, self.strings["afk_rate_limit_off"])
            elif afkrate_arg == "on":
                self._db.set(__name__, "afk_rate_limit", True)
                await utils.answer(message, self.strings["afk_rate_limit_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            afkrate_current = self._db.get(__name__, "afk_rate_limit")
            if afkrate_current is None or afkrate_current is False:
                self._db.set(__name__, "afk_rate_limit", True)
                await utils.answer(message, self.strings["afk_rate_limit_on"])
            elif afkrate_current is True:
                self._db.set(__name__, "afk_rate_limit", False)
                await utils.answer(message, self.strings["afk_rate_limit_off"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def allowcmd(self, message):
        """Allow this user to PM.\n """
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings["who_to_allow"])
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).union({user})))
        await utils.answer(message, self.strings["pm_allowed"].format(user))

    async def blockcmd(self, message):
        """Block this user to PM without being warned.\n """
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings["who_to_block"])
            return
        await message.client(functions.contacts.BlockRequest(user))
        await utils.answer(message, self.strings["pm_blocked"].format(user))

    async def denycmd(self, message):
        """Deny this user to PM without being warned.\n """
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings["who_to_deny"])
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).difference({user})))
        await utils.answer(message, self.strings["pm_denied"].format(user))

    async def pmcmd(self, message):
        """
        .pm : Disable/Enable automatic answer for denied PMs.
        .pm off : Disable automatic answer for denied PMs.
        .pm on : Enable automatic answer for denied PMs.
         
        """
        if utils.get_args_raw(message):
            pm_arg = utils.get_args_raw(message)
            if pm_arg == "off":
                self._db.set(__name__, "pm", True)
                await utils.answer(message, self.strings["pm_off"])
            elif pm_arg == "on":
                self._db.set(__name__, "pm", False)
                await utils.answer(message, self.strings["pm_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            pm_current = self._db.get(__name__, "pm")
            if pm_current is None or pm_current is False:
                self._db.set(__name__, "pm", True)
                await utils.answer(message, self.strings["pm_off"])
            elif pm_current is True:
                self._db.set(__name__, "pm", False)
                await utils.answer(message, self.strings["pm_on"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def pmlimitcmd(self, message):
        """
        .pmlimit : Get current max number of PMs before automatically block not allowed user.
        .pmlimit off : Disable automatic user blocking.
        .pmlimit on : Enable automatic user blocking.
        .pmlimit reset : Reset max number of PMs before automatically block not allowed user.
        .pmlimit [number] : Modify max number of PMs before automatically block not allowed user.
         
        """
        if utils.get_args_raw(message):
            pmlimit_arg = utils.get_args_raw(message)
            if pmlimit_arg == "off":
                self._db.set(__name__, "pm_limit", False)
                await utils.answer(message, self.strings["pm_limit_off"])
                return
            elif pmlimit_arg == "on":
                self._db.set(__name__, "pm_limit", True)
                pmlimit_on = self.strings["pm_limit_on"].format(self.get_current_limit())
                await utils.answer(message, pmlimit_on)
                return
            elif pmlimit_arg == "reset":
                self._db.set(__name__, "pm_limit_max", self.default_pm_limit)
                pmlimit_reset = self.strings["pm_limit_reset"].format(self.get_current_pm_limit())
                await utils.answer(message, pmlimit_reset)
                return
            else:
                try:
                    pmlimit_number = int(pmlimit_arg)
                    if pmlimit_number >= 10 and pmlimit_number <= 1000:
                        self._db.set(__name__, "pm_limit_max", pmlimit_number)
                        pmlimit_new = self.strings["pm_limit_set"].format(self.get_current_pm_limit())
                        await utils.answer(message, pmlimit_new)
                        return
                    else:
                        await utils.answer(message, self.strings["pm_limit_arg"])
                        return
                except ValueError:
                    await utils.answer(message, self.strings["pm_limit_arg"])
                    return
            await utils.answer(message, self.strings["limit_arg"])
        else:
            pmlimit = self._db.get(__name__, "pm_limit")
            if pmlimit is None or pmlimit is False:
                pmlimit_current = self.strings["pm_limit_current_no"]
            elif pmlimit is True:
                pmlimit_current = self.strings["pm_limit_current"].format(self.get_current_pm_limit())
            else:
                await utils.answer(message, self.strings["unknow"])
                return
            await utils.answer(message, pmlimit_current)

    async def pmnotifcmd(self, message):
        """
        .pmnotif : Disable/Enable the notifications from denied PMs.
        .pmnotif off : Disable the notifications from denied PMs.
        .pmnotif on : Enable the notifications from denied PMs.
         
        """
        if utils.get_args_raw(message):
            pmnotif_arg = utils.get_args_raw(message)
            if pmnotif_arg == "off":
                self._db.set(__name__, "pm_notif", False)
                await utils.answer(message, self.strings["pm_notif_off"])
            elif pmnotif_arg == "on":
                self._db.set(__name__, "pm_notif", True)
                await utils.answer(message, self.strings["pm_notif_on"])
            else:
                await utils.answer(message, self.strings["arg_on_off"])
        else:
            pmnotif_current = self._db.get(__name__, "pm_notif")
            if pmnotif_current is None or pmnotif_current is False:
                self._db.set(__name__, "pm_notif", True)
                await utils.answer(message, self.strings["pm_notif_on"])
            elif pmnotif_current is True:
                self._db.set(__name__, "pm_notif", False)
                await utils.answer(message, self.strings["pm_notif_off"])
            else:
                await utils.answer(message, self.strings["unknow"])

    async def reportcmd(self, message):
        """Report the user to spam. Use only in PM.\n """
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings["who_to_report"])
            return
        self._db.set(__name__, "allow", list(set(self._db.get(__name__, "allow", [])).difference({user})))
        if message.is_reply and isinstance(message.to_id, types.PeerChannel):
            await message.client(functions.messages.ReportRequest(peer=message.chat_id,
                                                                  id=[message.reply_to_msg_id],
                                                                  reason=types.InputReportReasonSpam()))
        else:
            await message.client(functions.messages.ReportSpamRequest(peer=message.to_id))
        await utils.answer(message, self.strings["pm_reported"])

    async def unblockcmd(self, message):
        """Unblock this user to PM."""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings["who_to_unblock"])
            return
        await message.client(functions.contacts.UnblockRequest(user))
        await utils.answer(message, self.strings["pm_unblocked"].format(user))

    async def watcher(self, message):
        user = await utils.get_user(message)
        pm = self._db.get(__name__, "pm")
        if getattr(message.to_id, "user_id", None) == self._me.user_id and (pm is None or pm is False):
            if not user.is_self and not user.bot and not user.verified and not self.get_allowed(message.from_id):
                await utils.answer(message, self.strings["pm_go_away"])
                if self._db.get(__name__, "pm_limit") is True:
                    pms = self._db.get(__name__, "pms", {})
                    pm_limit = self._db.get(__name__, "pm_limit_max")
                    pm_user = pms.get(message.from_id, 0)
                    if isinstance(pm_limit, int) and pm_limit >= 10 and pm_limit <= 1000 and pm_user >= pm_limit:
                        await utils.answer(message, self.strings["pm_triggered"])
                        await message.client(functions.contacts.BlockRequest(message.from_id))
                        await message.client(functions.messages.ReportSpamRequest(peer=message.from_id))
                        del pms[message.from_id]
                        self._db.set(__name__, "pms", pms)
                    else:
                        self._db.set(__name__, "pms", {**pms, message.from_id: pms.get(message.from_id, 0) + 1})
                pm_notif = self._db.get(__name__, "pm_notif")
                if pm_notif is None or pm_notif is False:
                    await message.client.send_read_acknowledge(message.chat_id)
                return
        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.user_id:
            afk_status = self._db.get(__name__, "afk")
            if user.is_self or user.bot or user.verified or afk_status is False:
                return
            if message.mentioned and self._db.get(__name__, "afk_no_group") is True:
                return
            afk_no_pm = self._db.get(__name__, "afk_no_pm")
            if getattr(message.to_id, "user_id", None) == self._me.user_id and afk_no_pm is True:
                return
            if self._db.get(__name__, "afk_rate_limit") is True:
                afk_rate = self._db.get(__name__, "afk_rate", [])
                if utils.get_chat_id(message) in afk_rate:
                    return
                else:
                    self._db.setdefault(__name__, {}).setdefault("afk_rate", []).append(utils.get_chat_id(message))
                    self._db.save()
            now = datetime.datetime.now().replace(microsecond=0)
            gone = datetime.datetime.fromtimestamp(self._db.get(__name__, "afk_gone")).replace(microsecond=0)
            diff = now - gone
            if afk_status is True:
                afk_message = self.strings["afk"].format(diff)
            elif afk_status is not False:
                afk_message = self.strings["afk_reason"].format(diff, afk_status)
            await utils.answer(message, afk_message)
            _notif = self._db.get(__name__, "_notif")
            if _notif is None or _notif is False:
                await message.client.send_read_acknowledge(message.chat_id)

    def get_allowed(self, id):
        return id in self._db.get(__name__, "allow", [])

    def get_current_pm_limit(self):
        pm_limit = self._db.get(__name__, "pm_limit_max")
        if not isinstance(pm_limit, int) or pm_limit < 10 or pm_limit > 1000:
            pm_limit = self.default_pm_limit
            self._db.set(__name__, "pm_limit_max", pm_limit)
        return pm_limit
