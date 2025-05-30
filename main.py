from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ChemGPT Spectroscopy Microservice",
    description="Handles all spectroscopy-related tasks for ChemGPT (UV, IR, etc.)",
    version="0.1.0"
)

# Enable CORS (open for now, restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "chemgpt-spectro", "message": "Spectroscopy microservice is alive!"}

@app.post("/spectroscopy")
async def spectroscopy_endpoint(request: Request):
    body = await request.json()
    # Example: expects {"molecule": "benzene"} or similar
    molecule = body.get("molecule", "")
    # Placeholder response (replace with real spectra logic)
    return {
        "molecule": molecule,
        "uv": {"peaks": [{"wavelength": 254, "intensity": "high"}]},  # dummy UV
        "ir": {"peaks": [{"wavenumber": 1600, "intensity": "strong"}]},  # dummy IR
        "message": "Spectra generated (dummy response)"
    }
