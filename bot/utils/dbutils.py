from datetime import datetime, timedelta
from typing import TypedDict

from sqlalchemy import or_, select, update
from sqlalchemy.dialects.postgresql import insert as postgreinsert

from bot.exceptions import MemberAlreadyChangedError
from bot.utils.misc import convert_jakarta
from database.core import session
from database.models.member_model import Booster, Member as MemberModel

BoosterDict = TypedDict(
    "BoosterDict", {"userid": int, "isboosting": bool, "boosting_since": datetime}
)


async def bulk_update_booster(members: list[BoosterDict]):
    ids = {member["userid"] for member in members}
    async with session.session_maker() as dbsession:
        await dbsession.execute(
            update(Booster).where(
                Booster.userid.not_in(ids), Booster.isboosting == True
            ),
            {"isboosting": False, "expired_since": datetime.now()},
        )
        await dbsession.execute(
            postgreinsert(Booster).on_conflict_do_nothing(),
            members,
        )
        await dbsession.execute(
            update(Booster),
            members,
        )
        await dbsession.commit()


async def update_booster(
    userid: int, status: bool, boosting_since: datetime | None = None
):
    if boosting_since:
        boosting_since = convert_jakarta(boosting_since)
    async with session.session_maker() as dbsession:
        booster = await dbsession.get(Booster, userid)
        if booster is None:
            booster = Booster(userid, boosting_since=boosting_since, isboosting=status)
            dbsession.add(booster)
        else:
            booster.isboosting = status
            if status:
                booster.boosting_since = boosting_since
            else:
                booster.expired_since = datetime.now()
        await dbsession.commit()
    return booster


async def get_valid_booster():
    async with session.session_maker() as dbsession:
        result = await dbsession.scalars(
            select(Booster)
            .where(
                or_(
                    Booster.isboosting,
                    Booster.expired_since >= (datetime.now() - timedelta(days=7)),
                )
            )
            .order_by(Booster.boosting_since.asc())
            .limit(20)
        )
        return result.all()


async def update_member(userid: int, ign: str, server: int):
    async with session.session_maker() as dbsession:
        member = await dbsession.get(MemberModel, userid)
        if member is None:
            member = MemberModel(userid=userid, ingame=ign, server=server)
            dbsession.add(member)
        elif member and member.has_changed is False:
            member.ingame = ign
            member.server = server
            member.has_changed = True
        else:
            raise MemberAlreadyChangedError(
                "You have already changed your data before!"
            )
        await dbsession.commit()


async def get_member_data(userid: int):
    async with session.session_maker() as dbsession:
        member = await dbsession.get(MemberModel, userid)
    return member
