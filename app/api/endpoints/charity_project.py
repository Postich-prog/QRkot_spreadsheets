from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_delete_project_invested_or_closed,
    check_info_none,
    check_name_duplicate,
    check_update_project_closed,
    check_update_project_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.donation import make_donation

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_info_none(charity_project.name, charity_project.description, session)
    await check_name_duplicate(charity_project.name, session)
    new_project = await charityproject_crud.create(charity_project, session)
    new_project = await make_donation(session, new_project)
    return new_project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charityproject_crud.get_multi(session)
    return all_projects


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_delete_project_invested_or_closed(project_id, session)
    charity_project = await charityproject_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_update_project_closed(project_id, session)
    await check_update_project_invested(charity_project, obj_in.full_amount)
    charity_project = await charityproject_crud.update(charity_project, obj_in, session)
    return charity_project
