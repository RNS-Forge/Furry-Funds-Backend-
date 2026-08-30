from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os
from pathlib import Path

from app.common.database import init_database
from app.common.auth_routes import router as auth_router
from app.operator.routes import router as operator_router
from app.manager.routes import router as manager_router
from app.admin.routes import router as admin_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection
    await init_database()
    yield
    # Cleanup

app = FastAPI(
    title="Furry Funds AI",
    description="A comprehensive system for managing domestic animal loan applications",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
from urllib.parse import urlparse

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [frontend_url, "http://localhost:5173", "http://localhost:5174"]
try:
    parsed = urlparse(frontend_url)
    if parsed.scheme and parsed.netloc:
        allowed_origins.append(f"{parsed.scheme}://{parsed.netloc}")
except Exception:
    pass

if "," in frontend_url:
    allowed_origins.extend([o.strip() for o in frontend_url.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(operator_router, prefix="/api/operator", tags=["Operator"])
app.include_router(manager_router, prefix="/api/manager", tags=["Manager"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

# Mount static files for uploads
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def root():
    return {"message": "Livestock Loan Eligibility System API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("DEBUG", True))
    )