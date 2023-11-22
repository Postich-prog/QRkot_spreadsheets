from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud


async def make_donation(
    session: AsyncSession,
    object,
):
    project, donation = await donation_crud.get_open_object(session)
    if not project or not donation:
        await session.commit()
        await session.refresh(object)
        return object

    num_donation = donation.full_amount - donation.invested_amount
    project_balance = project.full_amount - project.invested_amount

    if project_balance < num_donation:
        project.invested_amount += project_balance
        donation.invested_amount += project_balance
        project.fully_invested = True
        project.close_date = datetime.now()

    if project_balance > num_donation:
        project.invested_amount += num_donation
        donation.invested_amount += num_donation
        donation.fully_invested = True
        donation.close_date = datetime.now()

    if project_balance == num_donation:
        project.invested_amount += num_donation
        donation.invested_amount += num_donation
        project.fully_invested = True
        donation.fully_invested = True
        project.close_date = datetime.now()
        donation.close_date = datetime.now()

    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    await make_donation(session, object)
    return object
