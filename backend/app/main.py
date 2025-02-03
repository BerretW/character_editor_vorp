from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, characters

# Tímhle (pokud chceš) vytvoříš tabulky, když neexistují.
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Připojíme routery (prefix a "tagy" si nastav podle potřeby)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(characters.router, prefix="/characters", tags=["Characters"])
