import logging
import telethon
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class InactiveDetectorMod(loader.Module):
    """Detects inactive users"""
    strings = {
        "name": "Inactivity detector",
        "top_header": "These {un} users wrote {mn} messages or less since joining the group:\n\n",
        "top_place": "[{name}](tg://user?id={uid}) ({nmsg})",  # FIXME: mentions
        "top_delimiter": ", ",  # TODO: move to config
        "not_int": "<b>Most messages must be integer</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "default_chat_id", -1001457369532, "Chat ID to get top if command used in PM",
            "top_delimiter", ', ', "Separates inactivity top members"
        )
        self.name = self.strings['name']

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

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

        filt = ~(telethon.tl.alltlobjects.types.ChannelParticipantsBots
                 | telethon.tl.alltlobjects.types.ChannelParticipantsKicked)

        async for user in self.client.iter_participants(chat_id, filter=filt):
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

        await utils.answer(message, msg, parse_mode="md")

    async def watcher(self, message):
        if message.is_private:
            return
        else:
            chat_id = str(message.chat_id)
        users = self.db.get(__name__, chat_id, {})
        from_id = str(message.from_id)
        # this creates user if not exists
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
