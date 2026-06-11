from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Group
from app.schemas import GroupSummary, GroupTableResponse
from app.services.group_table_service import build_group_table

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[GroupSummary])
def list_groups(db: Session = Depends(get_db)) -> list[Group]:
    return list(db.scalars(select(Group).order_by(Group.code.asc())))


@router.get("/{group_code}", response_model=GroupSummary)
def get_group(group_code: str, db: Session = Depends(get_db)) -> Group:
    group = db.scalar(select(Group).where(Group.code == group_code.upper()))
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.get("/{group_code}/table", response_model=GroupTableResponse)
def get_group_table(group_code: str, db: Session = Depends(get_db)) -> GroupTableResponse:
    group = db.scalar(select(Group).where(Group.code == group_code.upper()))
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return build_group_table(db, group_code)

