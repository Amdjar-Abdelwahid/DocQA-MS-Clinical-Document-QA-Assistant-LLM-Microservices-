from fastapi import FastAPI
from api.routes import router as synthese_router

app = FastAPI(
    title="SyntheseComparative Microservice",
    version="1.0.0"
)

app.include_router(synthese_router, prefix="/api", tags=["synthese"])
