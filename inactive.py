import logging
import json
# import telethon
from .. import loader, utils, security

logger = logging.getLogger(__name__)


@loader.tds
class InactiveDetectorMod(loader.Module):
    """Detects inactive users"""
    strings = {
        "name": "Inactivity detector",
        "top_header": "These {un} users wrote {mn} messages or less since joining the group:\n\n",
        "top_place": "[{name}](tg://user?id={uid}) ({nmsg})",  # FIXME: mentions
        "top_delimiter": ", ",  # TODO: move to config
        "not_int": "<b>Most messages must be integer</b>",
        "recount_priv": "<b>I can't recount stats in private messages!</b>",
        "recount_started": "<b>Processing recount for chat {}. It may take a lot.</b>",
        "recount_db_dumped": "<b>Dumped database to owners and/or saved messages</b>",
        "recount_dump": "<b>Database dump for chat {cid}:<b>\n\n<pre>{dmp}</pre>",
        "recount_iter_done": "<b>Iterated over {} messages in this chat</b>",
        "recount_finish": "<b>Recount successful!</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "default_chat_id", -1001457369532, "Chat ID to get top if command used in PM",
            "top_delimiter", ', ', "Separates inactivity top members",
            "dump_db_before_recount", False, "Dump database of chat before recounting. "
                                             "Dump will be sent to saved or bot owners"
        )
        self.name = self.strings['name']

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.me = await self.client.get_me()

    async def inactivecmd(self, message):
        """.inactive <N>"""
        if message.is_private:
            chat_id = self.config['default_chat_id']
        else:
            chat_id = message.chat_id
        args = utils.get_args(message)
        if args:
            if args[0].isdigit():
                most = int(args[0])
            else:
                await utils.answer(message, self.strings("not_int", message))
                return
        else:
            most = 0
        users_db = self.db.get(__name__, str(chat_id), {})
        users = {}

        async for user in self.client.iter_participants(chat_id):
            if not user.bot:
                if str(user.id) not in users_db:
                    users_db[str(user.id)] = self.get_empty_user(user)
                users[str(user.id)] = users_db[str(user.id)]
            # We won't include users not CURRENTLY in chat,
            # but their stats will remain in the database

        self.db.set(__name__, str(chat_id), users_db)

        def key(x):
            return x[1]['cnt']

        users = sorted(users.items(), key=key)
        text = []
        for uid, u in users:
            if u['cnt'] <= most:
                text.append(self.strings('top_place', message).format(
                    name=u['name'], uid=uid, nmsg=u['cnt']
                ))
            else:
                break
        msg = self.strings('top_header', message).format(un=len(text), mn=most)\
            + self.config['top_delimiter'].join(text)

        kw = {}
        if self.me.id != message.from_id:
            kw['silent'] = True
        await utils.answer(message, msg, parse_mode="md", **kw)

    async def recountcmd(self, message):
        if message.is_private:
            await utils.answer(message, self.strings('recount_priv', message))
            return

        chat_id = message.chat_id
        await utils.answer(message, self.strings('recount_started', message).format(chat_id))
        db = self.db.get(__name__, str(chat_id), {})
        json_db = json.dumps(db)
        msg = self.strings("recount_dump", message).format(cid=chat_id, dmp=json_db)
        logging.debug('Database dump (chat %d): %s', chat_id, json_db)
        owners = self.db.get(security.__name__, "owner", ["me"])
        if owners:
            for owner in owners:
                try:
                    await self.client.send_message(owner, msg)
                except Exception:
                    logger.warning("Dump of chat %d sending to %d failed",
                                   chat_id, owner, exc_info=True)
        new_db = {}
        n = 0
        async for msg in self.client.iter_messages(chat_id, limit=None):
            if not msg.sender.bot:
                n += 1
                from_id = msg.from_id
                # Ensure such user exists, or create him
                new_db[str(from_id)] = new_db.get(str(from_id),
                                                  self.get_empty_user(msg.sender))
                new_db[str(from_id)]['cnt'] += 1
        await utils.answer(message, self.strings("recount_iter_done", message).format(n))
        self.db.set(__name__, str(chat_id), new_db)
        await utils.answer(message, self.strings("recount_finish", message))

    async def watcher(self, message):
        if message.is_private:
            return
        else:
            chat_id = str(message.chat_id)
        users = self.db.get(__name__, chat_id, {})
        from_id = str(message.from_id)
        # this creates user if not exists
        if message.sender:
            users[from_id] = users.get(from_id, self.get_empty_user(message.sender))
            users[from_id]["cnt"] += 1
            self.db.set(__name__, chat_id, users)

    def get_full_name(self, user):
        fn, ln = '', ''
        if user.first_name:
            fn = user.first_name
        if user.last_name:  # Can be None, then we get an exception
            ln = user.last_name
        return (fn + ' ' + ln).strip()

    def get_empty_user(self, user):
        return {"cnt": 0, "name": self.get_full_name(user)}
