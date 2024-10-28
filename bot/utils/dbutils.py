from datetime import datetime

from database.core import session
from database.models.member_model import Booster


async def update_booster(userid: int, status: bool):
    async with session.session_maker() as dbsession:
        booster = await dbsession.get(Booster, userid)
        if booster is None:
            booster = Booster(userid, boosting_since=datetime.now(), isboosting=status)
            dbsession.add(booster)
        else:
            booster.isboosting = status
            if status:
                booster.boosting_since = datetime.now()
            else:
                booster.expired_since = datetime.now()
        await dbsession.commit()
