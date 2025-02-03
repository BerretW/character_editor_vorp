from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from flask_mysqldb import MySQL
from flask import Flask

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:8080", # for vue.js
    # Add more here if needed
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

users_db = 'users.json' # Store users in json db.
def load_users():
    try:
        with open(users_db, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(users_db, 'w') as f:
        json.dump(users, f, indent=4)

def create_access_token(data: dict, expires_delta: timedelta):
   to_encode = data.copy()
   expire = datetime.utcnow() + expires_delta
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encoded_jwt

def authenticate_user(username, password):
    users = load_users()
    user = users.get(username)
    if user and user["password"] == password:
        return User(username=username, password=password)
    return False


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username = payload.get("sub")
      if username is None:
         raise credentials_exception
      token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users = load_users()
    if token_data.username in users:
        return token_data
    else:
         raise credentials_exception

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# MySQL Setup
app_flask = Flask(__name__)
# Konfigurace MySQL
app_flask.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app_flask.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app_flask.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app_flask.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app_flask.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app_flask)

# --- Models --- #
class CharacterModel(BaseModel):
    identifier: str
    steamname: str
    charidentifier: int
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
    LastLogin: Optional[str] = None
    inventory: Optional[dict] = None
    slots: float = 35.0
    job: str = "unemployed"
    joblabel: str = "job label"
    status: Optional[dict] = {}
    meta: Optional[dict] = {}
    firstname: str = " "
    lastname: str = " "
    character_desc: str = " "
    gender: str = " "
    age: int = 0
    nickname: str = " "
    skinPlayer: Optional[dict] = None
    compPlayer: Optional[dict] = None
    compTints: Optional[dict] = None
    jobgrade: int = 0
    coords: Optional[dict] = {}
    isdead: bool = False
    trust: int = 0
    walk: str = "noanim"
    crafting: Optional[dict] = {'medical':0,'blacksmith':0,'basic':0,'survival':0,'brewing':0,'food':0}
    info: Optional[dict] = {}
    gunsmith: float = 0.00
    ammo: Optional[dict] = {}
    discordid: Optional[str] = "0"
    lastjoined: Optional[List[str]] = []
    ranchid: Optional[int] = 0
 # -- Router -- #
def get_characters_from_db(page: int = 1, per_page: int = 10, search_term: Optional[str] = None) -> List[CharacterModel]:
    cur = mysql.connection.cursor()
    start = (page - 1) * per_page
    query = "SELECT * FROM characters"
    params = []
    if search_term:
         query += " WHERE firstname LIKE %s OR lastname LIKE %s OR nickname LIKE %s OR steamname LIKE %s"
         search_term = f"%{search_term}%"
         params.extend([search_term, search_term,search_term,search_term])

    query += " LIMIT %s, %s"
    params.extend([start, per_page])
    cur.execute(query, params)
    characters = cur.fetchall()
    cur.close()
    return characters

@app.get('/characters', response_model=List[CharacterModel], dependencies=[Depends(get_current_user)])
def list_characters(page: int = 1, per_page: int = 10, search: Optional[str] = None):
    characters = get_characters_from_db(page,per_page,search)
    return characters

@app.get('/characters/{charidentifier}', response_model=CharacterModel, dependencies=[Depends(get_current_user)])
def get_character(charidentifier: int):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM characters WHERE charidentifier = %s", (charidentifier,))
    character = cur.fetchone()
    cur.close()
    if character:
      return character
    else:
         raise HTTPException(status_code=404, detail="Character not found")

@app.put('/characters/{charidentifier}', response_model=CharacterModel, dependencies=[Depends(get_current_user)])
def update_character(charidentifier: int, data: CharacterModel):
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            UPDATE characters 
            SET 
                steamname=%s, `group`=%s, money=%s, gold=%s, rol=%s, xp=%s, healthouter=%s, healthinner=%s, staminaouter=%s, staminainner=%s, hours=%s,
                inventory=%s, slots=%s, job=%s, joblabel=%s, `status`=%s, meta=%s, firstname=%s, lastname=%s, character_desc=%s, gender=%s, age=%s, nickname=%s,
                skinPlayer=%s, compPlayer=%s, compTints=%s, jobgrade=%s, coords=%s, isdead=%s, `trust`=%s, `walk`=%s, crafting=%s, info=%s, gunsmith=%s, ammo=%s, discordid=%s, ranchid=%s
            WHERE charidentifier=%s
        """, (
            data.steamname, data.group, data.money, data.gold, data.rol, data.xp, data.healthouter, data.healthinner, data.staminaouter, data.staminainner, data.hours,
            json.dumps(data.inventory), data.slots, data.job, data.joblabel, json.dumps(data.status), json.dumps(data.meta), data.firstname, data.lastname, data.character_desc, data.gender, data.age, data.nickname,
            json.dumps(data.skinPlayer), json.dumps(data.compPlayer), json.dumps(data.compTints), data.jobgrade, json.dumps(data.coords), data.isdead, data.trust, data.walk, json.dumps(data.crafting), json.dumps(data.info), data.gunsmith, json.dumps(data.ammo), data.discordid, data.ranchid, charidentifier
        ))
        mysql.connection.commit()
    except Exception as e:
       raise HTTPException(status_code=400, detail="Error updating character: {}".format(e))
    cur.close()
    return data

@app.delete('/characters/{charidentifier}', dependencies=[Depends(get_current_user)])
def delete_character(charidentifier: int):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM characters WHERE charidentifier = %s", (charidentifier,))
    mysql.connection.commit()
    cur.close()
    return JSONResponse(content={'message': 'Character deleted successfully'})

@app.post('/characters/{charidentifier}/copy', response_model=CharacterModel, dependencies=[Depends(get_current_user)])
def copy_character(charidentifier: int, new_identifier: str):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM characters WHERE charidentifier = %s", (charidentifier,))
  character = cur.fetchone()
  if not character:
       cur.close()
       raise HTTPException(status_code=404, detail="Character not found")

  character.pop("charidentifier",None)
  try:
    cur.execute("""
        INSERT INTO characters (
          identifier, steamname, `group`, money, gold, rol, xp, healthouter, healthinner, staminaouter, staminainner, hours,
          inventory, slots, job, joblabel, `status`, meta, firstname, lastname, character_desc, gender, age, nickname,
          skinPlayer, compPlayer, compTints, jobgrade, coords, isdead, `trust`, `walk`, crafting, info, gunsmith, ammo, discordid, ranchid
           )
          VALUES (
           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
          )
          """, (
            new_identifier, character.get('steamname'), character.get('group'), character.get('money'), character.get('gold'), character.get('rol'), character.get('xp'), character.get('healthouter'), character.get('healthinner'), character.get('staminaouter'), character.get('staminainner'), character.get('hours'),
              json.dumps(character.get('inventory')), character.get('slots'), character.get('job'), character.get('joblabel'), json.dumps(character.get('status')), json.dumps(character.get('meta')), character.get('firstname'), character.get('lastname'), character.get('character_desc'), character.get('gender'), character.get('age'), character.get('nickname'),
              json.dumps(character.get('skinPlayer')), json.dumps(character.get('compPlayer')), json.dumps(character.get('compTints')), character.get('jobgrade'), json.dumps(character.get('coords')), character.get('isdead'), character.get('trust'), character.get('walk'), json.dumps(character.get('crafting')), json.dumps(character.get('info')), character.get('gunsmith'), json.dumps(character.get('ammo')), character.get('discordid'), character.get('ranchid')
           )
    )
    mysql.connection.commit()
    cur.execute("SELECT * FROM characters WHERE identifier = %s ORDER BY charidentifier DESC LIMIT 1",(new_identifier,))
    character = cur.fetchone()
  except Exception as e:
    cur.close()
    raise HTTPException(status_code=400, detail="Error copying character: {}".format(e))

  cur.close()
  return character

@app.post('/characters/{charidentifier}/move', response_model=CharacterModel, dependencies=[Depends(get_current_user)])
def move_character(charidentifier: int, new_identifier: str):
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE characters SET identifier = %s WHERE charidentifier = %s", (new_identifier, charidentifier))
        mysql.connection.commit()
        cur.execute("SELECT * FROM characters WHERE charidentifier = %s",(charidentifier,))
        character = cur.fetchone()
    except Exception as e:
        cur.close()
        raise HTTPException(status_code=400, detail="Error moving character: {}".format(e))
    cur.close()
    return character