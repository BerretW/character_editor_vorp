from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_

from ..database import get_db
from ..models import CharacterDB
from ..schemas import CharacterModel
from .auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CharacterModel])
def list_characters(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    query = db.query(CharacterDB)
    if search:
        query = query.filter(
            or_(
                CharacterDB.firstname.ilike(f"%{search}%"),
                CharacterDB.lastname.ilike(f"%{search}%"),
                CharacterDB.nickname.ilike(f"%{search}%"),
                CharacterDB.steamname.ilike(f"%{search}%"),
            )
        )
    offset_val = (page - 1) * per_page
    characters = query.offset(offset_val).limit(per_page).all()
    return characters

@router.get("/{charidentifier}", response_model=CharacterModel)
def get_character(charidentifier: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    character = db.query(CharacterDB).filter(CharacterDB.charidentifier == charidentifier).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.put("/{charidentifier}", response_model=CharacterModel)
def update_character(
    charidentifier: int,
    data: CharacterModel,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    character = db.query(CharacterDB).filter(CharacterDB.charidentifier == charidentifier).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Přepíšeme pole
    character.identifier = data.identifier
    character.steamname = data.steamname
    # ... a tak dále pro všechny sloupce ...
    character.ranchid = data.ranchid

    db.commit()
    db.refresh(character)
    return character

@router.delete("/{charidentifier}")
def delete_character(charidentifier: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    character = db.query(CharacterDB).filter(CharacterDB.charidentifier == charidentifier).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(character)
    db.commit()
    return {"message": "Character deleted successfully"}

@router.post("/{charidentifier}/copy", response_model=CharacterModel)
def copy_character(charidentifier: int, new_identifier: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    old_char = db.query(CharacterDB).filter(CharacterDB.charidentifier == charidentifier).first()
    if not old_char:
        raise HTTPException(status_code=404, detail="Character not found")

    new_char = CharacterDB(
        identifier=new_identifier,
        steamname=old_char.steamname,
        group=old_char.group,
        money=old_char.money,
        gold=old_char.gold,
        rol=old_char.rol,
        xp=old_char.xp,
        healthouter=old_char.healthouter,
        healthinner=old_char.healthinner,
        staminaouter=old_char.staminaouter,
        staminainner=old_char.staminainner,
        hours=old_char.hours,
        LastLogin=old_char.LastLogin,
        inventory=old_char.inventory,
        slots=old_char.slots,
        job=old_char.job,
        joblabel=old_char.joblabel,
        status=old_char.status,
        meta=old_char.meta,
        firstname=old_char.firstname,
        lastname=old_char.lastname,
        character_desc=old_char.character_desc,
        gender=old_char.gender,
        age=old_char.age,
        nickname=old_char.nickname,
        skinPlayer=old_char.skinPlayer,
        compPlayer=old_char.compPlayer,
        compTints=old_char.compTints,
        jobgrade=old_char.jobgrade,
        coords=old_char.coords,
        isdead=old_char.isdead,
        trust=old_char.trust,
        walk=old_char.walk,
        crafting=old_char.crafting,
        info=old_char.info,
        gunsmith=old_char.gunsmith,
        ammo=old_char.ammo,
        discordid=old_char.discordid,
        lastjoined=old_char.lastjoined,
        ranchid=old_char.ranchid
    )
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

@router.post("/{charidentifier}/move", response_model=CharacterModel)
def move_character(charidentifier: int, new_identifier: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    character = db.query(CharacterDB).filter(CharacterDB.charidentifier == charidentifier).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    character.identifier = new_identifier
    db.commit()
    db.refresh(character)
    return character
