import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Retrieve database URL from environment or use a local fallback
DATABASE_URL: str = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

engine = create_engine(DATABASE_URL, echo=True)

class Hero(SQLModel, table=True):
    """Represents a hero entity in the database."""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

class HeroUpdate(SQLModel):
    """Model for updating an existing hero with optional fields."""
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

def create_db_and_tables() -> None:
    """Creates the database tables based on the defined SQLModels."""
    SQLModel.metadata.create_all(engine)

def seed_initial_data() -> None:
    """Seeds the database with initial heroes if the table is empty."""
    with Session(engine) as session:
        statement = select(Hero)
        existing_heroes = session.exec(statement).all()
        
        match existing_heroes:
            case []:
                hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
                hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
                hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
                
                session.add(hero_1)
                session.add(hero_2)
                session.add(hero_3)
                session.commit()
            case _:
                pass  # Database is already populated

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handles startup and shutdown events for the FastAPI application."""
    create_db_and_tables()
    seed_initial_data()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/heroes", response_model=list[Hero])
def read_heroes() -> list[Hero]:
    """Retrieves all heroes from the database."""
    with Session(engine) as session:
        statement = select(Hero)
        heroes = session.exec(statement).all()
        return list(heroes)

@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int) -> Hero:
    """Retrieves a specific hero by their primary key.
    
    Raises:
        HTTPException: If the hero with the given ID does not exist.
    """
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        
        match hero:
            case None:
                raise HTTPException(status_code=404, detail="Hero not found")
            case _:
                return hero

@app.post("/heroes", response_model=Hero)
def create_hero(hero: Hero) -> Hero:
    """Adds a new hero to the database."""
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.patch("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_update: HeroUpdate) -> Hero:
    """Partially updates an existing hero.
    
    Raises:
        HTTPException: If the hero with the given ID does not exist.
    """
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        
        match db_hero:
            case None:
                raise HTTPException(status_code=404, detail="Hero not found")
            case _:
                update_data = hero_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(db_hero, key, value)
                
                session.add(db_hero)
                session.commit()
                session.refresh(db_hero)
                return db_hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int) -> dict[str, bool]:
    """Deletes a specific hero by their primary key.
    
    Raises:
        HTTPException: If the hero with the given ID does not exist.
    """
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        
        match hero:
            case None:
                raise HTTPException(status_code=404, detail="Hero not found")
            case _:
                session.delete(hero)
                session.commit()
                return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)