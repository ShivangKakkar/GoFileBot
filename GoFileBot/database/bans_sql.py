from sqlalchemy import Column, Integer, String
from . import BASE, SESSION


class Bans(BASE):
    __tablename__ = "bans"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True)
    reason = Column(String, nullable=True)

    def __init__(self, user_id, reason=None):
        self.user_id = user_id
        self.reason = reason


Bans.__table__.create(checkfirst=True)


async def num_banned():
    try:
        return SESSION.query(Bans).count()
    finally:
        SESSION.close()


async def all_banned():
    try:
        obj = SESSION.query(Bans).all()
        info = {}
        for o in obj:
            info[o.user_id] = o.reason
        return info
    finally:
        SESSION.close()


async def ban(user_id, reason=None):
    q = SESSION.query(Bans).get(user_id)
    if q:
        if reason:
            q.reason = reason
    else:
        SESSION.add(Bans(user_id, reason))
    SESSION.commit()


async def unban(user_id):
    q = SESSION.query(Bans).get(user_id)
    SESSION.delete(q)
    SESSION.commit()
