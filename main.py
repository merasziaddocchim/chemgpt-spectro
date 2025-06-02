from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI(
    title="ChemGPT Spectroscopy Microservice",
    description="Handles all spectroscopy-related tasks for ChemGPT (UV, IR, etc.)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "chemgpt-spectro", "message": "Spectroscopy microservice is alive!"}

class MoleculeRequest(BaseModel):
    molecule: str

# Get API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set!")

@app.post("/spectroscopy")
async def spectroscopy_endpoint(data: MoleculeRequest):
    molecule = data.molecule.strip()
    if not molecule:
        raise HTTPException(status_code=400, detail="Molecule name or SMILES required.")

    # Build GPT-4o prompt for spectra
    prompt = (
        f"You are a chemistry assistant. For the molecule '{molecule}', "
        "provide both the IR and UV-Vis spectra as markdown tables with typical experimental or literature values. "
        "If you don't have data, say 'Not available.' "
        "IR table: wavenumber (cm⁻¹), intensity, assignment. "
        "UV table: wavelength (nm), intensity, electronic transition type. "
        "Only give the tables, no intro."
    )

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=700
        )
        answer = response.choices[0].message.content
        return {
            "molecule": molecule,
            "spectra_markdown": answer,
            "source": "AI-generated spectra via GPT-4o"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
