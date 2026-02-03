from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# Create FastAPI instance
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: Routes
@app.get("/")
async def root():
    return {"message": "Welcome to the POS System!"}


@app.get("/health")
async def health():
    return {"status": "OK", "version": settings.APP_VERSION}