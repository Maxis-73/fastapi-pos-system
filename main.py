from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import Base, engine
from src.auth.routes import router as user_router
from src.categories.routes import router as categories_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creamos las tablas al arrancar la aplicación
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(user_router)
app.include_router(categories_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the POS System!"}

@app.get("/health")
async def health():
    return {"status": "OK", "version": settings.APP_VERSION}