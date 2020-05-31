# requires: pymongo dnspython

# Забейте
import asyncio
import pymongo

import logging
logger = logging.getLogger(__name__)
from .. import loader, utils

class Student:
    def __init__(self, id: int, last_name: str, first_name: str, 
                    patronymic: str, grade: int, region: str, academ: bool, approved: int=None):
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.grade = int(grade)
        self.region = region
        self.academ = bool(academ)
        self.approved = approved
        self.id = int(id)
    
    def __str__(self):
        p = 'Академ' if self.academ else 'Отбор'
        # a = f'Уже вроде бы добавлен в чат (tg://user?id={self.approved})' if self.approved else 'Еще нет в чате'
        return f'[{p}.{self.id}] {self.last_name} {self.first_name} {self.patronymic}, '\
        f'{self.grade} класс, из {self.region}'

class SiriusMod(loader.Module):
    """Ищем поступивших на ИЮ2020"""
    strings = {"name": "Sirius"}
    def __init__(self):
        self.config = loader.ModuleConfig(
            # name - default - description
            "db_uri", None, "Database URI, if you dont know where to take it - nevermind",
            "db_db", None, "database",
            "db_coll", None, "collection",
            "replace_ё", True, "replace ё with е in requests, incorrect usage may return incorrect result"
        )
        self.name = self.strings['name']
        self.db = None
    
    def config_complete(self):
        self.db = pymongo.MongoClient(self.config['db_uri'])\
            .get_database(self.config['db_db']).get_collection(self.config['db_coll'])

    async def findcmd(self, message):
        arg = utils.get_args_raw(message).strip()
        if self.config['replace_ё']:
            arg = arg.replace('ё', 'е')
            arg = arg.replace('Ё', 'Е')
        logger.debug('Got: %s', arg)
        if not arg:
            await utils.answer(message, 'Только 1 аргумент - номер в списке или фамилия/имя')
        if arg.isdigit():
            add = f'людей с номером {arg}'
            arg = int(arg)
            users = list(self.db.find({"id": arg}))
        elif ' ' in arg or arg.lower() == 'янао': # Костыли костыли
            add = f'людей из региона {arg}'
            _users = list(self.db.find())
            users = []
            for user in _users:
                if user['region'].lower() == arg.lower():
                    users.append(user)
        else:
            add = f'людей, которых зовут {arg}'
            arg = arg.capitalize()
            users = list(self.db.find({'$or': [{"last_name": arg}, {"first_name": arg}, {"patronymic": arg}]}))

        msg = [f'{len(users)} всего {add}', '==']
        for user in users:
            del user['_id']
            s = Student(**user)
            msg += [str(s), '==']
        msg = msg[:-1]
        msg = '\n'.join(msg)
        await utils.answer(message, msg)



