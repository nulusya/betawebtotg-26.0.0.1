import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Telegram Shop SaaS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}

# SPA Serving
# Assuming we run this from 'server/' directory and client is in '../client/dist'
CLIENT_DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "client", "dist")

if os.path.exists(CLIENT_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(CLIENT_DIST, "assets")), name="assets")

    @app.get("/")
    async def serve_spa_root():
        return FileResponse(os.path.join(CLIENT_DIST, "index.html"))

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            return {"error": "API route not found"}
        
        file_path = os.path.join(CLIENT_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
             return FileResponse(file_path)
        
        return FileResponse(os.path.join(CLIENT_DIST, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Client build not found. Run 'npm run build' in client directory."}
