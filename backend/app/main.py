from fastapi import FastAPI
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, characters

# Tímhle (pokud chceš) vytvoříš tabulky, když neexistují.
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tady můžeš omezit na ["http://localhost:5173"] apod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Připojíme routery (prefix a "tagy" si nastav podle potřeby)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(characters.router, prefix="/characters", tags=["Characters"])
