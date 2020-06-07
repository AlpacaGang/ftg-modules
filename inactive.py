import logging

from .. import loader, utils  # noqa: F401

logger = logging.getLogger(__name__)


@loader.tds
class InactiveDetectorMod(loader.Module):
    """Detects inactive users"""
    strings = {
        "name": "Inactivity detector",
        "top_header": "These {un} users wrote {mn} messages or less since joining the group:\n\n",
        "top_place": "[{name}](tg://user?id={uid}) ({nmsg})",
        "top_delimiter": ", ",
        "not_int": "<b>Most messages must be integer</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "default_chat_id", -1001457369532, "Chat ID to get top if command used in PM"
        )
        self.name = self.strings['name']

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def inactivecmd(self, message):
        """.inactive """
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
        else:
            most = 0
        users = self.db.get(__name__, chat_id, {})

        def key(x):
            return x[1]['cnt']

        users = dict(sorted(users.items(), key=key))
        text = []
        for uid in users:
            u = users[uid]
            if u['cnt'] <= most:
                text.append(self.strings('top_place', message).format(
                    name=u['name'], uid=uid, nmsg=u['cnt']
                ))
            else:
                break
        msg = self.strings('top_header', message).format(un=len(text), mn=most)\
            + self.strings('top_delimiter', message).join(text)

        await utils.answer(message, msg)

    async def watcher(self, message):
        if message.is_private:
            return
        else:
            chat_id = message.chat_id
        users = self.db.get(__name__, chat_id, {})
        from_id = message.from_id
        # this creates user if not exists
        users[from_id] = users.get(from_id,
                                   {"cnt": 0,
                                    "name": message.sender.first_name + ' '
                                    + message.sender.last_name})
        users[from_id]["cnt"] += 1
        self.db.set(__name__, chat_id, users)
