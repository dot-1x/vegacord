from datetime import datetime, timedelta
from typing import Literal, Sequence, TypedDict, overload

from sqlalchemy import or_, select, update
from sqlalchemy.dialects.postgresql import insert as postgreinsert

from bot.exceptions import MemberAlreadyChangedError, MemberUnchanged
from bot.utils.misc import convert_jakarta
from database.core import session
from database.models.member_model import Booster, Member as MemberModel

BoosterDict = TypedDict(
    "BoosterDict", {"userid": int, "isboosting": bool, "boosting_since": datetime}
)

BoosterData = TypedDict(
    "BoosterData", {"found": Sequence[MemberModel], "notfound": set[int]}
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
                booster.expired_since = None
            else:
                booster.expired_since = booster.expired_since or datetime.now()
        await dbsession.commit()
    return booster


@overload
async def get_valid_booster(with_data: Literal[False] = False) -> Sequence[Booster]: ...


@overload
async def get_valid_booster(with_data: Literal[True]) -> BoosterData: ...


async def get_valid_booster(with_data=False) -> Sequence[Booster] | BoosterData:
    async with session.session_maker() as dbsession:
        result = await dbsession.scalars(
            select(Booster)
            .where(Booster.isboosting)
            .order_by(Booster.boosting_since.asc())
            .limit(20)
        )
        if not with_data:
            return result.all()
        members = result.all()
        members_id = {member.userid for member in members}
        res_data = await dbsession.scalars(
            select(MemberModel).where(MemberModel.userid.in_(members_id))
        )
        data = res_data.all()
        data_id = {user.userid for user in data}
        return {"found": data, "notfound": members_id - data_id}


async def update_member(userid: int, ign: str, server: int):
    async with session.session_maker() as dbsession:
        member = await dbsession.get(MemberModel, userid)
        if member is None:
            member = MemberModel(userid=userid, ingame=ign, server=server)
            dbsession.add(member)
        elif member.ingame == ign.strip() and member.server == server:
            raise MemberUnchanged("Your data remains the same as before")
        elif member.has_changed is False:
            member.ingame = ign
            member.server = server
            member.has_changed = True
        else:
            raise MemberAlreadyChangedError(
                "You have already changed your data before!"
            )
        await dbsession.commit()
    return member


async def get_member_data(userid: int):
    async with session.session_maker() as dbsession:
        member = await dbsession.get(MemberModel, userid)
    return member
