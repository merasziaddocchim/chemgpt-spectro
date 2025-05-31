from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Define the request body model
class MoleculeRequest(BaseModel):
    molecule: str

@app.post("/spectroscopy")
async def spectroscopy_endpoint(data: MoleculeRequest):
    molecule = data.molecule
    # Placeholder response (replace with real spectra logic)
    return {
        "molecule": molecule,
        "uv": {"peaks": [{"wavelength": 254, "intensity": "high"}]},  # dummy UV
        "ir": {"peaks": [{"wavenumber": 1600, "intensity": "strong"}]},  # dummy IR
        "message": "Spectra generated (dummy response)"
    }
