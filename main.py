from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI(title="PALI Suite Hub")

# Ensure packages directory exists
PACKAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packages")

@app.get("/download/{os_type}")
async def download_package(os_type: str):
    file_map = {
        "windows": "PALI_2_Windows.zip",
        "mac": "PALI_2_Mac.zip",
        "linux": "PALI_2_Linux.zip"
    }
    
    file_name = file_map.get(os_type.lower())
    if not file_name:
        raise HTTPException(status_code=404, detail="OS type not supported")
        
    file_path = os.path.join(PACKAGES_DIR, file_name)
    
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="PALI2.zip", # Force rename to PALI2.zip
            media_type='application/zip'
        )
    else:
        raise HTTPException(status_code=404, detail=f"File not found on server: {file_name}")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"))

# Mount assets if they exist
assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
