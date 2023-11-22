from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    meeting_room = await charityproject_crud.get(charity_project_id, session)
    if meeting_room is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return meeting_room


async def check_delete_project_invested_or_closed(
    project_id: int,
    session: AsyncSession,
):
    charity_project = await charityproject_crud.get(obj_id=project_id, session=session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


async def check_update_project_closed(
    project_id: int,
    session: AsyncSession,
):
    charity_project = await charityproject_crud.get(obj_id=project_id, session=session)
    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать!",
        )
    return charity_project


async def check_update_project_invested(
    project,
    new_full_amount,
):
    if new_full_amount:
        if new_full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="При редактировании проекта нельзя "
                "устанавливать требуемую сумму меньше внесённой.",
            )
    return project


async def check_info_none(
    name: str,
    desc: str,
    session: AsyncSession,
) -> None:
    if name is None or desc is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Field can not be None",
        )
