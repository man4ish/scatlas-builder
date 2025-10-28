from fastapi import FastAPI
from app.database import Base, engine
from app.routers import upload, integrate, visualize

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Single-Cell Atlas Builder", version="0.1.0")

app.include_router(upload.router)
app.include_router(integrate.router)
app.include_router(visualize.router)


@app.get("/")
def root():
    return {"message": "Single-Cell Atlas Builder API is running"}
