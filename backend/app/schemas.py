from pydantic import BaseModel
from typing import Optional
from datetime import date  # přidej import

class CharacterModel(BaseModel):
    charidentifier: int
    identifier: str
    steamname: str
    group: str = "user"
    money: float = 0.00
    gold: float = 0.00
    rol: float = 0.00
    xp: int = 0
    healthouter: int = 500
    healthinner: int = 100
    staminaouter: int = 100
    staminainner: int = 100
    hours: float = 0
    LastLogin: Optional[date] = None  # změněno z Optional[str]
    inventory: Optional[str] = None
    slots: float = 35.0
    job: str = "unemployed"
    joblabel: str = "job label"
    status: str = "{}"
    meta: str = "{}"
    firstname: str = " "
    lastname: str = " "
    character_desc: str = " "
    gender: str = " "
    age: int = 0
    nickname: str = " "
    skinPlayer: Optional[str] = None
    compPlayer: Optional[str] = None
    compTints: Optional[str] = None
    jobgrade: int = 0
    coords: str = "{}"
    isdead: bool = False
    trust: int = 0
    walk: str = "noanim"
    crafting: str = '{"medical":0,"blacksmith":0,"basic":0,"survival":0,"brewing":0,"food":0}'
    info: str = "{}"
    gunsmith: float = 0.00
    ammo: str = "{}"
    discordid: str = "0"
    lastjoined: str = "[]"
    ranchid: int = 0
    
    class Config:
        from_attributes = True
