from fastapi import FastAPI
from app.routes import image_routes

app = FastAPI()

# Include routes for image processing
app.include_router(image_routes.router)
